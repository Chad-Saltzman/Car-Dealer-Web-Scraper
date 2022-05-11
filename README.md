Car Dealer Web Scraper  (CS491 DevOps and Testing)

Final Project Application Pipeline

Tech Stack:
  Source Control - Github
  CI/CD tool - Jenkins
  Automated Testing - Python Unit Tests. This is called through a Jenkins Job which is queued when a commit occurs or when manually built
  Automated Deployment - Jenkins will deploy a Docker Image to Docker Hub to the container chadas1108/web_scraper
  
 If you wanted to replicate the CI/CD Environment. I created an EC2 machine in AWS and deployed a jenkins server on that. Once Jenkins was deployed I added a job to automate the build and deployment.
  
 In order for this application to run integration tests and main driver the following installations are required:
    chrome_driver - https://sites.google.com/a/chromium.org/chromedriver/downloads
        Chrome Driver allows selenium to create a headless chrome browser to browse websites and gather html data for the web scraper
    Once the chrome_driver is installed make sure it is added to your environment path and you are setup to run the application.
 
 To run the application Tests:
   docker run chadas1108/web_scraper
      This will run both the unit tests on the application. 
      
   To run the integration tests you will have to pull the code base and run the integration tests with the command "python3 WebScraperIntegrationTest.py"
      
 To run the application Main Driver:
    git clone https://github.com/Chad-Saltzman/Car-Dealer-Web-Scraper.git
    run the command python3 WebScraper.py  
       
   

