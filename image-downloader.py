import requests
from PIL import Image
from tqdm import tqdm
from colorama import Fore, Style, init
import os
import shutil

# Initialize colorama for Windows support
init()

def center_text(text):
    terminal_width = shutil.get_terminal_size().columns
    return text.center(terminal_width)

def imgshow(file_location_with_name):
    try:
        img = Image.open(file_location_with_name)
        img.show()
    except Exception as e:
        print(f"{Fore.RED}Error displaying image: {e}{Style.RESET_ALL}")

def imgdown(url, file_location):
    local_filename = url.split('/')[-1]
    full_path = os.path.join(file_location, local_filename)
    
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(full_path, 'wb') as f:
                total_size = int(r.headers.get('content-length', 0))
                chunk_size = 1024
                for chunk in tqdm(r.iter_content(chunk_size=chunk_size), total=total_size//chunk_size, unit='KB'):
                    f.write(chunk)
        print(f"{Fore.GREEN}\nDownload completed!{Style.RESET_ALL}")
        imgshow(full_path)
        display_image_metadata(full_path)  # Display metadata after download
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error downloading the image: {e}{Style.RESET_ALL}")

def imgdown_batch(urls, file_location):
    for url in urls:
        imgdown(url, file_location)

def convert_image_format(file_path, target_format):
    try:
        img = Image.open(file_path)
        base = os.path.splitext(file_path)[0]
        new_file_path = base + f".{target_format.lower()}"
        img.save(new_file_path, target_format.upper())
        print(f"{Fore.GREEN}Image converted to {target_format} and saved as {new_file_path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error converting image: {e}{Style.RESET_ALL}")

def resize_image(file_path, new_width, new_height):
    try:
        img = Image.open(file_path)
        resized_img = img.resize((new_width, new_height))
        resized_img.save(file_path)
        print(f"{Fore.GREEN}Image resized to {new_width}x{new_height} and saved.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error resizing image: {e}{Style.RESET_ALL}")

def display_image_metadata(file_path):
    try:
        img = Image.open(file_path)
        print(f"{Fore.YELLOW}Image Metadata:")
        print(f"File: {file_path}")
        print(f"Format: {img.format}")
        print(f"Size: {img.size} pixels")
        print(f"Mode: {img.mode}")
        print(f"Color Palette: {img.palette}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error displaying image metadata: {e}{Style.RESET_ALL}")

def print_menu():
    print(f"{Fore.CYAN}{center_text('--- Online Image Downloader ---')}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{center_text('1. Download a Single Image')}")
    print(f"{Fore.YELLOW}{center_text('2. Download Multiple Images')}")
    print(f"{Fore.YELLOW}{center_text('3. Convert Image Format')}")
    print(f"{Fore.YELLOW}{center_text('4. Resize Image')}")
    print(f"{Fore.YELLOW}{center_text('5. Display Image Metadata')}")
    print(center_text("6. Exit"))
    print(f"{Style.RESET_ALL}")

def main():
    while True:
        print_menu()
        choice = input(f"{Fore.CYAN}\nEnter your choice (1-6): {Style.RESET_ALL}")
        
        if choice == '1':
            url = input(f"{Fore.CYAN}\nEnter the URL of the image: {Style.RESET_ALL}")
            file_location = input(f"{Fore.CYAN}Enter the directory where you want to save the image: {Style.RESET_ALL}")
            
            if not os.path.exists(file_location):
                os.makedirs(file_location)
                print(f"{Fore.GREEN}Directory {file_location} created.{Style.RESET_ALL}")
            
            if file_location[-1] != '\\':
                file_location = file_location + '\\'
            
            imgdown(url, file_location)

        elif choice == '2':
            urls = input(f"{Fore.CYAN}\nEnter the URLs of the images (comma-separated): {Style.RESET_ALL}").split(',')
            file_location = input(f"{Fore.CYAN}Enter the directory where you want to save the images: {Style.RESET_ALL}")
            
            if not os.path.exists(file_location):
                os.makedirs(file_location)
                print(f"{Fore.GREEN}Directory {file_location} created.{Style.RESET_ALL}")
            
            if file_location[-1] != '\\':
                file_location = file_location + '\\'
            
            imgdown_batch(urls, file_location)

        elif choice == '3':
            file_path = input(f"{Fore.CYAN}\nEnter the file path of the image you want to convert: {Style.RESET_ALL}")
            target_format = input(f"{Fore.CYAN}Enter the target format (e.g., JPEG, PNG): {Style.RESET_ALL}")
            convert_image_format(file_path, target_format)
        
        elif choice == '4':
            file_path = input(f"{Fore.CYAN}\nEnter the file path of the image you want to resize: {Style.RESET_ALL}")
            new_width = int(input(f"{Fore.CYAN}Enter the new width: {Style.RESET_ALL}"))
            new_height = int(input(f"{Fore.CYAN}Enter the new height: {Style.RESET_ALL}"))
            resize_image(file_path, new_width, new_height)
        
        elif choice == '5':
            file_path = input(f"{Fore.CYAN}\nEnter the file path of the image to display metadata: {Style.RESET_ALL}")
            display_image_metadata(file_path)
        
        elif choice == '6':
            print(f"{Fore.GREEN}\nThank you for using the Image Downloader! Goodbye!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}\nInvalid choice. Please select a number between 1 and 6.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
