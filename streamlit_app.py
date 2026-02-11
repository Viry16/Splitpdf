import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import io
import zipfile
import os

st.set_page_config(page_title="PDF Splitter", page_icon="✂️")

st.title("✂️ PDF Splitter for GitHub")
st.markdown("Upload a large PDF file, and this tool will split it into smaller chunks suitable for GitHub uploads.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")
    
    # PDF Info
    try:
        reader = PdfReader(uploaded_file)
        total_pages = len(reader.pages)
        st.info(f"Total Pages: {total_pages}")
        
        # Settings
        split_method = st.radio("Select Split Method:", ["By Chunk Size", "Extract Single Pages (1 file per page)"])
        
        if split_method == "Extract Single Pages (1 file per page)":
             pages_per_chunk = 1
             st.info(f"This will extract all pages as {total_pages} individual files.")
        else:
             default_chunk_size = min(50, total_pages)
             pages_per_chunk = st.number_input("Pages per chunk", min_value=1, max_value=total_pages, value=default_chunk_size)
        
        if st.button("Split PDF"):
            progress_bar = st.progress(0)
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                base_name = os.path.splitext(uploaded_file.name)[0]
                
                for i in range(0, total_pages, pages_per_chunk):
                    writer = PdfWriter()
                    chunk_start = i
                    chunk_end = min(i + pages_per_chunk, total_pages)
                    
                    for page_num in range(chunk_start, chunk_end):
                        writer.add_page(reader.pages[page_num])
                    
                    # Write chunk to memory
                    chunk_buffer = io.BytesIO()
                    writer.write(chunk_buffer)
                    chunk_buffer.seek(0)
                    
                    # Add to zip
                    chunk_filename = f"{base_name}_part_{i // pages_per_chunk + 1}.pdf"
                    zip_file.writestr(chunk_filename, chunk_buffer.getvalue())
                    
                    # Update progress
                    progress = min((i + pages_per_chunk) / total_pages, 1.0)
                    progress_bar.progress(progress)
            
            zip_buffer.seek(0)
            
            st.success("Splitting complete! Download your files below.")
            
            st.download_button(
                label="Download Split Files (ZIP)",
                data=zip_buffer,
                file_name=f"{base_name}_split.zip",
                mime="application/zip"
            )

            st.divider()
            st.subheader("GitHub Helper")
            st.markdown("If you are running this locally, you can save directly to a folder and delete the original.")
            
            if st.button("Save to 'output' folder"):
                 output_dir = "output"
                 if not os.path.exists(output_dir):
                     os.makedirs(output_dir)
                 
                 # Re-process to save files (since we only zipped in memory before)
                 for i in range(0, total_pages, pages_per_chunk):
                    writer = PdfWriter()
                    chunk_start = i
                    chunk_end = min(i + pages_per_chunk, total_pages)
                    
                    for page_num in range(chunk_start, chunk_end):
                        writer.add_page(reader.pages[page_num])
                    
                    output_filename = f"{base_name}_part_{i // pages_per_chunk + 1}.pdf"
                    output_path = os.path.join(output_dir, output_filename)
                    
                    with open(output_path, "wb") as f:
                        writer.write(f)
                 
                 st.success(f"Files saved to '{os.path.abspath(output_dir)}'")
                 st.info("You can now `git add output/` to push these files.")
            
            # Check if file exists properly to offer deletion
            # Note: file_uploader doesn't give full path, so we check process cwd
            potential_path = os.path.join(os.getcwd(), uploaded_file.name)
            if os.path.exists(potential_path):
                 if st.button(f"DELETE original file '{uploaded_file.name}'"):
                     os.remove(potential_path)
                     st.warning(f"Deleted '{uploaded_file.name}' from disk. It won't be pushed to GitHub.")
            else:
                st.caption(f"Could not find '{uploaded_file.name}' in current folder to offer deletion.")

    except Exception as e:
        st.error(f"Error processing PDF: {e}")
