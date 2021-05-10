# Vaccine slot tracker

Uses CoWIN api to fetch vaccine availability information. Checkout all the APIs [here](https://apisetu.gov.in/public/marketplace/api/cowin).

## Steps to setup 

### A. Create a SNS topic for notification
1. Go to Simple Notification Service on AWS.
2. Create a standard topic.
3. Go to the newly created topic and create a subscription.
4. Select protocol as **http** and add your email as the endpoint.

### B. Create a lambda function
1. Manually copy code inside `lambda_function.py` or use upload from .zip file option on the right of the code editor.
2. Change the `district_id` (line 66) or `pincode` (line 67) as per your requirement.
3. Change the `TopicArn` on (line 55) to your newly created SNS topic ARN.
4. Deploy the code.

### C. Give lambda required permissions
1. Go to the lambda role inside IAM that was automatically created by AWS.
2. Attach the SNS **publish** policy to the role.

### D. Add layer to your lambda function
To use python `requests` library, you will have to create a lambda layer.
1. Go to *layers* on the lambda dashboard.
2. Click on *create layer*.
3. Upload the `python.zip` file from this repo and create the layer.
4. Go to the lambda function and add this layer.

### E. Test the function
1. You can test the function at this stage. 
2. If the vaccines are available, you'll get an email.
3. If you get any error, you can troubleshoot the code.

### F. Add a trigger to your lambda
1. On the lambda function overview, click on **Add trigger**.
2. Create a new rule.
3. Use schedule expression - `rate(1 hour)`, `cron(30 0-16/2 * * ? *)`.

This should work! 

Raise an issue if there are any concerns.
