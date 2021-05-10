import json
import datetime
import boto3
import requests     # gets the requests module from lambda layer

# filter important details in json
def extract_details_json(json, min_age):
    details = {}
    details['name'] = json.get('name', '')
    details['block_name'] = json.get('block_name', '')
    details['pincode'] = json.get('pincode', '')
    details['fee_type'] = json.get('fee_type', '')
    
    sessions = json.get('sessions', [])
    availability = 0
    vaccine = ''
    for session in sessions:
        # usually all sessions have same vaccine
        vaccine = session.get('vaccine', '')
        if session['min_age_limit'] == min_age:
            availability += session['available_capacity']
    
    details['sessions'] = len(sessions)
    details['total_availability'] = availability
    details['vaccine'] = vaccine
    
    return details

# filter important details in readable format
def extract_details_string(json, min_age):
    details = '-> Address: {} - {}\n' + \
              '    Fee: {} - Vaccine: {}\n' + \
              '    Sessions: {} - Slots: {}\n'
    
    name = json.get('name', '')
    pincode = json.get('pincode', '')
    fee = json.get('fee_type', '')
    
    sessions = json.get('sessions', [])
    availability = 0
    vaccine = ''
    for session in sessions:
        vaccine = session.get('vaccine', '')    # usually all sessions have same vaccine
        vaccine = '\U0001F937' if vaccine == '' else vaccine
        if session['min_age_limit'] == min_age:
            availability += session['available_capacity']
    
    return details.format(name, pincode, fee,
                        vaccine, len(sessions), availability)
        
# publish to sns    
def notify(payload):
    client = boto3.client('sns')
    response = client.publish(
        TopicArn='arn:aws:sns:ap-south-1:750562860253:vaccine-notifier',
        Message=str(payload),
        Subject='All available vaccine appointments.',
        MessageStructure='string')
    
def lambda_handler(event, context):
    # get tomorrow's date
    date = datetime.date.today() + datetime.timedelta(1)
    date = date.strftime("%d-%m-%Y")
    
    # agra district id and pincode
    district_id = '622'
    pincode = '282007'
    
    # search by 'pincode' or 'district'
    search_by = 'district'
    
    min_age_limit = 18
    min_capacity = 0
    
    # needed to bypass '403 forbidded' error while using scripts
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15'
    header = {'user-agent': user_agent}
    # request fetches result for the whole week i.e. from date to date+7 days
    if search_by == 'district':
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}"
        response = requests.get(url.format(district_id, date), headers=header)
    else:
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}"
        response = requests.get(url.format(pincode, date), headers=header)
    
    # return if api error encountered
    if response.status_code != 200:
        print('Error while fetching appointments - {}'.format(response.reason))
        return {
            'statusCode': response.status_code,
            'body': response.reason
        }

    result = json.loads(response.text)
    
    # search appointments
    appointments = ''
    for center in result['centers']:
        for session in center['sessions']:
            if session['min_age_limit'] == min_age_limit and session['available_capacity'] > min_capacity:
                appointments += extract_details_string(center, min_age_limit)
                break
            
    if appointments == '':
        print('No appointments found.')
        return {
            'statusCode': 404,
            'body': 'No appointments found.'
        }

    # send message to sns topic
    notify(appointments)

    print('Appointments published successfully.')
    return {
        'statusCode': 200,
        'body': 'Appointments published successfully.'
    }
