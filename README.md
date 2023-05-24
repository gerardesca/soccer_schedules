# Soccer Schedules
Web Scraping and Twitter Posting of soccer broadcasts

## Description
This project aims to automate the process of obtaining the television stations in which the soccer matches will be broadcast, filtering the information, generating an image and posting it on Twitter. By using web scraping techniques, the project extracts the necessary data from the target website and formats it into a visually appealing image. The generated image is then posted on Twitter to provide users with up-to-date information on available soccer streams.

## Features
Web scraping: The project utilizes web scraping techniques to extract relevant data from the target website.
Data filtering: Extracted data is filtered and processed to obtain specific information about football live streams.
Image generation: The project generates visually appealing images containing the filtered data to provide an informative representation of available live streams.
Twitter integration: The generated images are automatically posted on Twitter to reach a wider audience and provide real-time updates on football live streams.

### Installation
Clone the repository to your local machine.
Install the required dependencies by running pip install -r requirements.txt.
Set up the necessary API credentials in keys_.py.
Rename keys_.py to keys.py

### Configuration
To configure the project, you need to:

Customize the font path in settings.py
Set up Twitter API credentials in the configuration file to enable posting on Twitter.
Change the soccer leagues you want and the countries of transmission in the file database_utils.py

### Contributing
Contributions are welcome! If you have any suggestions, feature requests, or bug reports, please open an issue or submit a pull request.