<div align="center">
  <h1>Youtube Downloader</h1>
</div>

<div align="justify">
   This script a Python tool that let to search and download   videos from YouTube, as well as download the selected video as an audio file. Video search is carried out in 2 ways: by link, by keyword. This script is simple and easy to use. 
</div>

<br><br>

<div align="center">

# Settings
To use it, you need to complete the following steps:

<br>

### 📁 Clone this repository

   ```
   git clone https://github.com/lazycatcoder/YouTube-Downloader.git
   ```

<br>

### 📦 Install dependencies
   
   ```
   pip install -r requirements.txt
   ```

<br>

### 🔧 Additional Information
<div align="left">
For the script to work correctly, you will need a web driver that can be downloaded from the <a href="https://www.selenium.dev/documentation/en/webdriver/driver_requirements">Selenium</a> official website.  
</div>

<br>

<div align="left">
Specify the path to the downloaded web driver:

<br>

   ```
   driver=webdriver.Chrome(executable_path=r"chromedriver.exe", options=options)
   ```

<br>

🔴 It is important to note that if you use the keyword search, the "num_elems" variable shows how many searched elements will be displayed in the console, the default is 10, which means that a list of the first 10 found videos will be displayed, in order to increase or decrease this list, you need to make changes to the variable "num_elems". Also keep in mind that if too large a value is specified, the script execution may be delayed in time.

</div>