# frontend/app.py
import streamlit as st
import requests
import os

# Configuration - Use environment variable for API URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Research Hub - Qdrant Powered",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Research Hub - Powered by Qdrant")
st.markdown("""
Semantic search for academic papers using **Qdrant Vector Database**  
*All services running in Docker containers*
""")

# Display connection info
with st.sidebar:
    st.info(f"API URL: {API_BASE_URL}")
    
    # Health check
    try:
        health_response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if health_response.status_code == 200:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Connection Failed")
    except:
        st.error("❌ Cannot reach API")

st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox(
    "Choose Mode",
    ["Search Papers", "Add New Paper", "Similar Papers", "System Info"]
)

if app_mode == "Search Papers":
    st.header("🔍 Semantic Paper Search")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input("Enter your research question:", 
                            placeholder="e.g., 'Recent advances in transformer architectures'")
    
    with col2:
        limit = st.number_input("Results limit:", min_value=1, max_value=50, value=10)
    
    category_filter = st.selectbox(
        "Filter by category (optional):",
        ["", "cs.AI", "cs.LG", "cs.CV", "cs.CL", "cs.NE", "stat.ML"]
    )
    
    if st.button("🔍 Search Papers", type="primary") and query:
        with st.spinner("Searching papers..."):
            search_data = {
                "query": query,
                "limit": limit,
                "category_filter": category_filter if category_filter else None
            }
            
            try:
                response = requests.post(f"{API_BASE_URL}/search/", json=search_data, timeout=30)
                
                if response.status_code == 200:
                    results = response.json()
                    
                    st.success(f"Found {results['total_found']} papers for: '{results['query']}'")
                    
                    for i, paper in enumerate(results["results"]):
                        with st.expander(f"📄 **{paper['title']}** (Score: `{paper['score']:.4f}`)"):
                            st.write(f"**Abstract:** {paper['abstract']}")
                            st.write(f"**Authors:** {', '.join(paper['authors'])}")
                            st.write(f"**Categories:** {', '.join(paper['categories'])}")
                            st.code(f"Paper ID: {paper['id']}")
                else:
                    st.error(f"Error searching papers: {response.text}")
                    
            except requests.exceptions.Timeout:
                st.error("Search timeout - please try again")
            except Exception as e:
                st.error(f"Connection error: {e}")

elif app_mode == "Add New Paper":
    st.header("📝 Add New Research Paper")
    
    with st.form("add_paper_form"):
        st.subheader("Paper Details")
        
        title = st.text_input("Paper Title*")
        abstract = st.text_area("Abstract*", height=200,
                              placeholder="Enter the paper abstract here...")
        authors = st.text_input("Authors (comma-separated)*", 
                              placeholder="John Doe, Jane Smith, ...")
        publication_date = st.date_input("Publication Date")
        categories = st.multiselect(
            "Categories",
            ["cs.AI", "cs.LG", "cs.CV", "cs.CL", "cs.NE", "stat.ML", "cs.SE"]
        )
        
        submitted = st.form_submit_button("📤 Add Paper to Database", type="primary")
        
        if submitted:
            if not title or not abstract or not authors:
                st.error("❌ Please fill all required fields (*)")
            else:
                paper_data = {
                    "title": title,
                    "abstract": abstract,
                    "authors": [author.strip() for author in authors.split(",")],
                    "publication_date": str(publication_date),
                    "categories": categories
                }
                
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/papers/", 
                        json=paper_data,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"✅ Paper added successfully!")
                        st.info(f"**Paper ID:** `{result['paper_id']}`")
                        st.info(f"**Embedding Size:** {result['embedding_size']} dimensions")
                    else:
                        st.error(f"Error adding paper: {response.text}")
                        
                except Exception as e:
                    st.error(f"Connection error: {e}")

elif app_mode == "Similar Papers":
    st.header("🔍 Find Similar Papers")
    
    paper_id = st.text_input("Enter Paper ID:")
    limit = st.number_input("Number of similar papers:", min_value=1, max_value=20, value=5)
    
    if st.button("🔍 Find Similar Papers", type="primary") and paper_id:
        with st.spinner("Finding similar papers..."):
            try:
                response = requests.get(
                    f"{API_BASE_URL}/papers/similar/{paper_id}?limit={limit}",
                    timeout=30
                )
                
                if response.status_code == 200:
                    results = response.json()
                    
                    st.success(f"Found {results['total_found']} papers similar to: `{results['similar_to']}`")
                    
                    for paper in results["results"]:
                        with st.expander(f"📄 **{paper['title']}** (Similarity: `{paper['score']:.4f}`)"):
                            st.write(f"**Abstract:** {paper['abstract'][:500]}...")
                            st.code(f"Paper ID: {paper['id']}")
                else:
                    st.error("Paper not found or error in search")
                    
            except Exception as e:
                st.error(f"Connection error: {e}")

elif app_mode == "System Info":
    st.header("📊 System Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**Qdrant Vector DB**\n\n- Port: 6333\n- Storage: Persistent Volume")
    
    with col2:
        st.info("**FastAPI Backend**\n\n- Port: 8000\n- Auto-reload: Enabled")
    
    with col3:
        st.info("**Streamlit Frontend**\n\n- Port: 8501\n- Hot-reload: Enabled")
    
    # Test connections
    st.subheader("Connection Status")
    
    try:
        health_response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if health_response.status_code == 200:
            st.success("✅ All systems operational!")
            health_data = health_response.json()
            st.json(health_data)
        else:
            st.error("❌ API health check failed")
    except Exception as e:
        st.error(f"❌ Health check failed: {e}")

# Footer
st.markdown("---")
st.markdown("""
**Built with:**  
🔹 Qdrant Vector Database  
🔹 FastAPI Backend  
🔹 Streamlit Frontend  
🔹 Sentence Transformers  
🔹 Docker Containers
""")