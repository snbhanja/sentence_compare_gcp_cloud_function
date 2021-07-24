This repo has source code and steps for deploying sentence comparision function to google cloud function.

# Files:
function-source.zip
We will upload this zip file to gcloud function.
This zip has main.py and requirements.txt file  <br/>

main.py This file is for you reference and has the actual code for sentence comparision.  <br/>

requirements.txt This file has the required python packages and their version for cloud function environment. When cloud function getting deployed, it will install packages mentioned in this file.

# The steps to deploy in Google cloud function as below:

1. Signup for Google cloud platform account. There is free credit of 300$ for new signups. After signup and login, the home screen will like this,
![Google cloud platform home screen](images/00_homepage_gcp.png)

2. Click on "Search" as shown below,
![Google cloud platform Search](images\01_click_onSearch.PNG)

3. Type "Cloud run" and click on Click on "Cloud Run API" from search suggestion
![](images/02_search_cloud_run.PNG)

4. Enable Cloud run API.
![](images/03_cloud_run_api_enable.PNG) 

5. Click on back button.
![](images/04_click_on_back_button.PNG) 

6. Type "function" in Search box and click on "Cloud Functions" in suggestions.
![](images/05_search_function.PNG) 

7. Click on "CREATE FUNCTION"
![](images/06_create_function.PNG) 

8. Now you can see the form to create cloud function. Enter "Function name". Select "Region", this is automatically selected. 
![](images/07_create_func_form_part1.PNG) 

9. Select "Trigger" type as "HTTP". Select "Require Authentication". Check "Require HTTPS". Click on "save".
![](images/08_form_part2.PNG) 

10. Click on next.
![](images/09_click_next.PNG) 

11. Next screen will show like this.
![](images/10_func_part2.PNG) 

12. Select Runtime as "Python 3.7" and entry point as "sentence_compare". "sentence_compare" is the main function in main.py
![](images/11_select_runtime_entry_point.PNG) 

13. Select Zip
![](images/12_select_zip_upload.PNG) 

14. Browse function_source.zip file and select storage bucket.
![](images/13_browse_zip_file_select_cloud_storage.PNG) 

15. It should look like this after selecting zip file and storage bucket. 
![](images/14_after_uplaoding_zip.PNG) 

16. Click on Deploy
![](images/15_click_on_deploy.PNG) 

17. It will show, "function-3" currectly deploying with a circle running to the left
![](images/16_function_3_deploying.PNG) 

18. If deploy is success then you will see green check mark.
![](images/17_deploy_success_green.PNG) 

19. Click on function "function-3". It will show details of "function-3" cloud function. 
![](images/18_function3_home.PNG) 

20. Click on "Trigger" tab. This is the API url for this cloud function.
![](images/19_trigger_url.PNG) 

21. As we enbaled authentication while creating cloud function, we have to generate the auth key for this API. We will use this auth key with the API url. To generate auth key lets go to cloud shell.
![](images/20_click_on_cloud_shell.PNG) 

22. Run the below command in gcloud shell,
```shell
gcloud auth print-identity-token
```
![](images/21_enter_this_command_for_security_token.PNG) 

23. Click on Authorize, when asked. You will get a long string, use this token as your Basic auth .
![](images/22_click_on_authorize.PNG) 

24. If gcloud login not happened, then you may see error like this
![](images/23_gcloud_login_error.PNG) 

25. Enter below command to login to "gcloud"
```shell
gcloud auth login
```
It will generate a URL for you. Click on the URL and login with your cloud account
![](images/24_gcloud_auth_login.PNG) 

26. One login successful, it will show a code, copy this code
![](images/25_once_login_paste_this_code_in_gcloud_shell.PNG) 

27. Paste the copied code in glcoud shell as below
![](images/26_enter_verif_code.PNG) 

28. Then again enter the first auth command as below,
```shell
gcloud auth print-identity-token
```
![](images/27_success_login_then_again_token_command.PNG) 

29. Copy the autherization token generated above.
![](images/28_final_code.PNG) 

30. Run the script call_api_with_bearer_auth.py
Edit the "url" which is cloud function "Trigger URL".
In "payload" pass the input josn.
In "headers", in "Authorization" paste the auth key from gcloud shell after "Bearer" as shown in code below.
The code for calling API as below. 
Replace "******" with the auth code you copied from cloud shell.

```python
import requests
import json

url = "https://us-central1-braided-lambda-320710.cloudfunctions.net/function-3"

payload = json.dumps({
  "given_answer": "Although rose you feel pain now",
  "correct_answer": "All right, Ross. Look, you're feeling a lot of pain right now"
})
headers = {
  'Authorization': 'Bearer ******',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

```

The result as below,
![](images/28_final_result.PNG) 


31. You can also test this in google cloud itself,
When in "function-3" window, click on "TESTING" tab, enter the input JSON object and click on "TEST THE FUNCTION".
![](images/29_test_in_cloud_func.PNG) 

32. You can see the cloud function results as below,
![](images/30_cloud_result.PNG) 

33. You can also test this in POSTMAN. <br/>
Select "POST" <br/>
Enter the "Trigger URL" in url section. <br/>
Click on "Authorization". <br/>
Select "Bearer Token" from drop down. <br/>
Click on "Body", select "raw", select "JSON"
Paste the input json in the body section. <br/>
Click on "SEND"

![](images/31_postman_aith.PNG) 

34. You can the response from google cloud function as below,
![](images/32_postman_body_result.PNG)