from flask import Flask, render_template
import ninjarmmpy

app = Flask(__name__)

# Create our client
# Assuming we are storing our keys in environment variables we can access
client = ninjarmmpy.Client(
    AccessKeyID='YourAccessKeyID',
    SecretAccessKey='YourSecretAccessKey',
    Europe=False
)

@app.route('/')
def home():

    #Call the API data and store it 
    devices_list = client.get_devices()
    org_list = client.get_organizations()
    controllers = client.get_raid_controllers()
    device_dets = client.get_devices_detailed()
    #setting this for conversion
    raid_info = controllers['results']
    #Containers for extracted data
    server_info = []
    server_offline_data = []
    #Loops through API data and stores it into above object
    for org_stuff in org_list:
        org_id = org_stuff['id']
        org_name = org_stuff['name']
        for device_data in devices_list:   
            device_list = device_data['id']
            org_list = device_data['organizationId']
            sys_name = device_data['systemName']
            device_type = device_data['nodeClass']
            for raid_data in raid_info:
                device_id= raid_data['deviceId']
                raid_health = raid_data['systemHealthStatus']
                if org_id == org_list and device_list == device_id and raid_health == 'Need Attention':
                    if device_type == 'WINDOWS_SERVER':
                        to_server_info = {'Server_Name': device_data['systemName'], 'Company_Name': org_stuff['name']}
                        server_info.append(to_server_info)
    # Gets the Number of Servers needing attention
    y = 0
    for stuff in server_info:
        y = y + 1

    org_list = client.get_organizations()

#Loop through API data to find offline servers
    for org_stuff in org_list:
        org_id = org_stuff['id']
        org_name = org_stuff['name']
        for device_name in device_dets:
            device_num = device_name['id']
            comp_name = device_name['systemName']
            comp_type = device_name['nodeClass']
            comp_org = device_name['organizationId']
            comp_offline = device_name['offline']
            if comp_org == org_id and comp_type == 'WINDOWS_SERVER' and bool(comp_offline):
                gathered_data = {'Server_Name': device_name['systemName'], 'Company_Name': org_stuff['name']}
                server_offline_data.append(gathered_data)
    # Gets the Number of servers offline
    x = 0
    for things in server_offline_data:
            x = x + 1

    return render_template('index.html', x = x, y = y, server_info = server_info, server_offline_data = server_offline_data)

if __name__ == '__main__':
    app.run(debug=True)