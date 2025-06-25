import requests
import os

def get_file_paths(directory):
    """
    Retrieves all file paths in the specified directory.

    Args:
        directory (str): Path to the directory from which to retrieve file paths.
    Returns:
        file_paths (list of str): List of file paths in the directory.
    """
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

def send_file_to_url(file_path, url):
    """
    Sends a file to the specified URL using a POST request with multipart/form-data.
    
    Args:
        file_path (str): Path to the file to be sent.
        url (str): URL to which the file will be sent.
    Returns:
        response.txt (str): response from the server. --> hopefully markdown text
    """
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, files=files)
    
    return response.text

def convert_files_to_markdown(file_path_list, url):
    """
    Converts multiple files to markdown by sending them to the specified URL and then exports them to individual files.
    
    Args:
        file_paths (list of str): list of file paths to be converted.
        url (str): URL to which the files will be sent.
    Returns: 
        markdown_files (list of str): list of markdown file names that contain a converted file.
    """
    markdown_files = []
    for file_path in file_path_list:
        response_text = send_file_to_url(file_path, url)
        if response_text:
            markdown_file_name = f"{file_path}.md"
            with open(markdown_file_name, 'w') as markdown_file:
                markdown_file.write(response_text)
            markdown_files.append(markdown_file_name)
            print(f"Converted {file_path} to {markdown_file_name}")

    return markdown_files

if __name__ == "__main__":
    directory = "/Users/isabeltilles/Library/Mobile Documents/com~apple~CloudDocs/DoclingTestFiles"
    url = input("Enter URL to send files to: ")

    file_paths = get_file_paths(directory)
    if not file_paths:
        print("No files found in the specified directory.")
    else:
        markdown_files = convert_files_to_markdown(file_paths, url)
        print(f"Converted files to markdown: {markdown_files}")
        print("Conversion complete.")