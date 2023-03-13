# YouTube Downloader

import os
import sys
from datetime import datetime
from pytube import YouTube
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
import time


user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36']

options=webdriver.ChromeOptions()
options.add_argument(f"user-agent={random.choice(user_agents)}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless")  # Web driver running in the background


# Initialize the list for all found elements
all_elems = []


while True:
    download_type = input("\nSelect download type: \n 1. Download from link \n 2. Search by name \n 3. Exit \n Your choice: ")
    
    if download_type == "1":
        while True:
            # Request video URL
            url = input("Enter video URL: ")
            
            # Format selection
            choice = int(input("Select format: \n 1. Video \n 2. Audio \n 3. Return to start \n 4. Exit \n Your choice: "))

            # If a video is selected, prompt to select a quality
            if choice == 1:
                print("Select quality: \n 1. 1080p \n 2. 720p")
                while True:
                    try:
                        quality_choice = int(input("Your choice (1 or 2): "))
                        if quality_choice not in (1, 2):
                            print("Invalid value selected. Try again.")
                        else:
                            break
                    except ValueError:
                        print("Invalid input. Try again.")

                if quality_choice == 1:
                    stream = YouTube(url).streams.filter(res="1080p").first()
                elif quality_choice == 2:
                    stream = YouTube(url).streams.filter(res="720p").first()
                else:
                    print("Invalid value selected. End of the program.")
                    sys.exit()

                # Create download directory and download video
                directory = "./youtube/" + datetime.today().strftime('%Y-%m-%d')
                if not os.path.exists(directory):
                    os.makedirs(directory)
                filename = stream.default_filename
                if os.path.exists(directory + '/' + filename):
                    i = 1
                    while os.path.exists(directory + '/' + f"({i}){filename}"):
                        i += 1
                    filename = f"({i}){filename}"
                stream.download(output_path=directory, filename=filename) 
                print("Video downloaded successfully.", directory)

            # If audio is selected, download audio in highest quality
            elif choice == 2:
                stream = YouTube(url).streams.get_audio_only()

                # Create download directory and download audio
                directory = "./youtube/" + datetime.today().strftime('%Y-%m-%d')
                if not os.path.exists(directory):
                    os.makedirs(directory)
                filename = stream.default_filename
                if os.path.exists(directory + '/' + filename):
                    i = 1
                    while os.path.exists(directory + '/' + f"({i}){filename}"):
                        i += 1
                    filename = f"({i}){filename}"
                stream.download(output_path=directory, filename=filename)
                print("Audio downloaded successfully.", directory)
            
            elif choice == 3:
                break

            elif choice == 4:
                print("End of the program.")
                sys.exit() 

            else:
                print("Invalid value selected. End of the program.")
                sys.exit()
            
            # Continue or return to the beginning
            choice_return_link = int(input("\nMake a choice: \n 1. Continue \n 2. Return to the beginning \n 3. Exit \n Your choice: "))

            # Selection result
            if choice_return_link == 1:
                continue
            elif choice_return_link == 2:
                break
            elif choice_return_link == 3:
                print("End of the program.")
                sys.exit()  
            else:
                print("Invalid value selected. End of the program.")
                sys.exit()
            
    elif download_type == "2":
        
        query = str(input("Enter the title: "))
        url = f"https://www.youtube.com/results?search_query={query}"

        driver=webdriver.Chrome(executable_path=r"chromedriver.exe", options=options)

        driver.get(url)

        # Number of elements to look for
        num_elems = 10    

        while True:
            # Create an intermediate list
            temp_elems = []

            # Scroll down the page
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)

            driver.implicitly_wait(3)
            # time.sleep(1)
            
            # Find all div elements with class tittle
            elems = driver.find_elements(By.XPATH, "//ytd-video-renderer[@class='style-scope ytd-item-section-renderer']")

            # Add the found elements to the intermediate list 'temp_elems'
            for i, elem in enumerate(elems, start=1):
                title_elem = elem.find_element(By.ID, "video-title")
                title = title_elem.get_attribute("title")
                url = title_elem.get_attribute("href")
                
                temp_elems.append({"num": i, "title": title, "url": url})

            # If the number of elements in the intermediate list 'temp_elems' is less than 'num_elems', continue the loop
            if len(temp_elems) < num_elems:
                continue

            # Add the first 'num_elems' elements to the 'all_elems' list and stop the loop
            all_elems.extend(temp_elems[:num_elems])
            break

        driver.close()
        driver.quit()
        

        while True:
            # Print a list of all found elements
            for elem in all_elems:
                print(elem["num"], "-", elem["title"])

            # Prompt user to select a video
            while True:
                try:
                    selected_num = int(input("Enter video number to download: "))
                    if selected_num < 1 or selected_num > len(all_elems):
                        print("Wrong number. Try again.")
                    else:
                        selected_video = all_elems[selected_num - 1]
                        break
                except ValueError:
                    print("Invalid input. Please try again.")

            # Format selection
            choice = int(input("Select format: \n 1. Video \n 2. Audio \n 3. Return to start \n 4. Exit \n Your choice: "))

            # If a video is selected, prompt to select a quality
            if choice == 1:
                print("Select quality: \n 1. 1080p \n 2. 720p")
                while True:
                    try:
                        quality_choice = int(input("Your choice (1 or 2): "))
                        if quality_choice not in (1, 2):
                            print("Invalid value selected. Try again.")
                        else:
                            break
                    except ValueError:
                        print("Invalid input. Try again.")

                # Download the selected video using Pytube
                url = selected_video["url"]
                
                if quality_choice == 1:
                    stream = YouTube(url).streams.filter(res="1080p").first()
                elif quality_choice == 2:
                    stream = YouTube(url).streams.filter(res="720p").first()

                # Create download directory and download video
                directory = "./youtube/" + datetime.today().strftime('%Y-%m-%d')
                if not os.path.exists(directory):
                    os.makedirs(directory)
                filename = stream.default_filename
                if os.path.exists(directory + '/' + filename):
                    i = 1
                    while os.path.exists(directory + '/' + f"({i}){filename}"):
                        i += 1
                    filename = f"({i}){filename}"
                stream.download(output_path=directory, filename=filename) 
                print("Video downloaded successfully.", directory)
            
            # If audio is selected, download audio in highest quality
            elif choice == 2:
                url = selected_video["url"]
                stream = YouTube(url).streams.get_audio_only()
                
                # Create download directory and download audio
                directory = "./youtube/" + datetime.today().strftime('%Y-%m-%d')
                if not os.path.exists(directory):
                    os.makedirs(directory)
                filename = stream.default_filename
                if os.path.exists(directory + '/' + filename):
                    i = 1
                    while os.path.exists(directory + '/' + f"({i}){filename}"):
                        i += 1
                    filename = f"({i}){filename}"
                stream.download(output_path=directory, filename=filename)
                print("Audio downloaded successfully.", directory)
            
            elif choice == 3:
                break
            
            elif choice == 4:
                print("End of the program.")
                sys.exit()
            
            else:
                print("Invalid value selected. End of the program.")
                sys.exit()

            # Continue or return to the beginning
            choice_return_word = int(input("\nMake a choice: \n 1. Continue \n 2. Return to the beginning \n 3. Exit \n Your choice: "))

            # Selection result
            if choice_return_word == 1:
                continue
            elif choice_return_word == 2:
                break
            elif choice_return_word == 3:
                print("End of the program.")
                sys.exit()  
            else:
                print("Invalid value selected. End of the program.")
                sys.exit()

    elif download_type == "3":
        print("End of the program.")
        sys.exit()    

    else:
        print("Invalid value selected. End of the program.")
        sys.exit()