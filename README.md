# Vaccine slot tracker

Uses CoWIN api to fetch vaccine availability information. Checkout all the APIs [here](https://apisetu.gov.in/public/marketplace/api/cowin).

## Steps to setup 
1. Create a lambda function.
2. Manually copy code inside `lambda_function.py` or use upload from .zip file option on the right of the code editor.
3. Change the `district_id` (line 66) or `pincode` (line 67) as per your requirement.
4. Deploy the code.
5. To use python `requests` library, you will have to create a lambda layer.
    - Go to *layers* on the lambda dashboard.
    - Click on *create layer*.
    - Upload the `python.zip` file from this repo and create the layer.
    - Go to the lambda function and add this layer.
