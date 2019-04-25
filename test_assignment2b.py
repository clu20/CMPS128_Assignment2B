import unittest
import requests
import time
import os

######################## initialize variables ################################################
subnetName = "assignment2b-net"
subnetAddress = "10.10.0.0/16"

mainInstanceName = "main-instance"
forwardingInstance1Name = "forwarding-instance1"
forwardingInstance2Name = "forwarding-instance2"

ipAddressMainInstance = "10.10.0.2"
hostPortMainInstance = "8082"

ipAddressForwarding1Instance = "10.10.0.3"
hostPortForwarding1Instance = "8083"

ipAddressForwarding2Instance = "10.10.0.4"
hostPortForwarding2Instance = "8084"

############################### Docker Linux Commands ###########################################################
def removeSubnet(subnetName):
    command = "docker network rm " + subnetName + " &> /dev/null"
    os.system(command)

def createSubnet(subnetAddress, subnetName):
    command  = "docker network create --subnet=" + subnetAddress + " " + subnetName + " &> /dev/null"
    os.system(command)

def buildDockerImage():
    command = "docker build -t assignment2b-img ."
    os.system(command)

def runMainInstance(hostPortNumber, ipAddress, subnetName, instanceName):
    command = "docker run -d -p " + hostPortNumber + ":8080 --net=" + subnetName + " --ip=" + ipAddress + " --name=" + instanceName + " assignment2b-img" + " &> /dev/null"
    os.system(command)

def runForwardingInstance(hostPortNumber, ipAddress, subnetName, instanceName, forwardingAddress):
    command = "docker run -d -p " + hostPortNumber + ":8080 --net=" + subnetName  + " --ip=" + ipAddress + " --name=" + instanceName + " -e FORWARDING_ADDRESS=" + forwardingAddress + " assignment2b-img" + " &> /dev/null"
    os.system(command)

def stopAndRemoveInstance(instanceName):
    stopCommand = "docker stop " + instanceName + " &> /dev/null"
    removeCommand = "docker rm " + instanceName + " &> /dev/null"
    os.system(stopCommand)
    time.sleep(1)
    os.system(removeCommand)

################################# Unit Test Class ############################################################

class TestHW2(unittest.TestCase):

    ######################## Functions to send the required requests ##########################################
    def send_all_requests(self, baseUrl):
        # get nonexistent key
        response = requests.get(baseUrl + '/key-value-store/subject1')
        responseInJson = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(responseInJson['doesExist'], False)
        self.assertEqual(responseInJson['message'], 'Error in GET')
        self.assertEqual(responseInJson['error'], 'Key does not exist')

        # delete nonexistent key
        response = requests.delete(baseUrl + '/key-value-store/subject1')
        responseInJson = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(responseInJson['doesExist'], False)
        self.assertEqual(responseInJson['message'], 'Error in DELETE')
        self.assertEqual(responseInJson['error'], 'Key does not exist')

        # put nonexistent key
        response = requests.put(baseUrl + '/key-value-store/' + "subject1", json={'value': "Data Structures"})
        responseInJson = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(responseInJson['message'], 'Added successfully')
        self.assertEqual(responseInJson['replaced'], False)

        # get after putting nonexistent key
        response = requests.get(baseUrl + '/key-value-store/subject1')
        responseInJson = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(responseInJson['doesExist'], True)
        self.assertEqual(responseInJson['message'], 'Retrieved successfully')
        self.assertEqual(responseInJson['value'], 'Data Structures')

        # put existent key
        response = requests.put(baseUrl + '/key-value-store/' + "subject1", json={'value': "Distributed Systems"})
        responseInJson = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(responseInJson['message'], 'Updated successfully')
        self.assertEqual(responseInJson['replaced'], True)

        # get after putting existent key
        response = requests.get(baseUrl + '/key-value-store/subject1')
        responseInJson = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(responseInJson['doesExist'], True)
        self.assertEqual(responseInJson['message'], 'Retrieved successfully')
        self.assertEqual(responseInJson['value'], 'Distributed Systems')

        # delete existent key
        response = requests.delete(baseUrl + '/key-value-store/subject1')
        responseInJson = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(responseInJson['doesExist'], True)
        self.assertEqual(responseInJson['message'], 'Deleted successfully')

        # get after deleting key
        response = requests.get(baseUrl + '/key-value-store/subject1')
        responseInJson = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(responseInJson['doesExist'], False)
        self.assertEqual(responseInJson['message'], 'Error in GET')
        self.assertEqual(responseInJson['error'], 'Key does not exist')

        # put key with no value
        response = requests.put(baseUrl + '/key-value-store/subject1', json={})
        responseInJson = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(responseInJson['message'], 'Error in PUT')
        self.assertEqual(responseInJson['error'], 'Value is missing')

    def send_forwarding12_requests(self, baseUrl1, baseUrl2):
        # put nonexistent key
        response = requests.put(baseUrl1 + '/key-value-store/' + "subject1", json={'value': "Data Structures"})
        responseInJson = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(responseInJson['message'], 'Added successfully')
        self.assertEqual(responseInJson['replaced'], False)

        # get after putting nonexistent key
        response = requests.get(baseUrl2 + '/key-value-store/subject1')
        responseInJson = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(responseInJson['doesExist'], True)
        self.assertEqual(responseInJson['message'], 'Retrieved successfully')
        self.assertEqual(responseInJson['value'], 'Data Structures')

        # put existent key
        response = requests.put(baseUrl2 + '/key-value-store/' + "subject1", json={'value': "Distributed Systems"})
        responseInJson = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(responseInJson['message'], 'Updated successfully')
        self.assertEqual(responseInJson['replaced'], True)

        # get after putting existent key
        response = requests.get(baseUrl1 + '/key-value-store/subject1')
        responseInJson = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(responseInJson['doesExist'], True)
        self.assertEqual(responseInJson['message'], 'Retrieved successfully')
        self.assertEqual(responseInJson['value'], 'Distributed Systems')

        # delete existent key
        response = requests.delete(baseUrl1 + '/key-value-store/subject1')
        responseInJson = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(responseInJson['doesExist'], True)
        self.assertEqual(responseInJson['message'], 'Deleted successfully')

        # get after deleting key
        response = requests.get(baseUrl2 + '/key-value-store/subject1')
        responseInJson = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(responseInJson['doesExist'], False)
        self.assertEqual(responseInJson['message'], 'Error in GET')
        self.assertEqual(responseInJson['error'], 'Key does not exist')

    def send_requests_forwarding_while_main_stopped(self, baseUrl):

        # put nonexistent key
        response = requests.put(baseUrl + '/key-value-store/' + "subject1", json={'value': "Data Structures"})
        responseInJson = response.json()
        self.assertEqual(response.status_code, 503)
        self.assertEqual(responseInJson['message'], 'Error in PUT')
        self.assertEqual(responseInJson['error'], 'Main instance is down')


        # get after putting nonexistent key
        response = requests.get(baseUrl + '/key-value-store/subject1')
        responseInJson = response.json()
        self.assertEqual(response.status_code, 503)
        self.assertEqual(responseInJson['message'], 'Error in GET')
        self.assertEqual(responseInJson['error'], 'Main instance is down')

        # delete existent key
        response = requests.delete(baseUrl + '/key-value-store/subject1')
        responseInJson = response.json()
        self.assertEqual(response.status_code, 503)
        self.assertEqual(responseInJson['message'], 'Error in DELETE')
        self.assertEqual(responseInJson['error'], 'Main instance is down')

    ######################## Build docker image and create subnet ################################
    # build docker image
    buildDockerImage()

    # stop the containers using the subnet
    stopAndRemoveInstance(mainInstanceName)
    stopAndRemoveInstance(forwardingInstance1Name)
    stopAndRemoveInstance(forwardingInstance2Name)

    # remove the subnet possibly created from the previous run
    removeSubnet(subnetName)

    # create subnet
    createSubnet(subnetAddress, subnetName)


    ########################## Run tests #######################################################
    def test_a_all_running_request_main(self):

        print("\nRunning all instances and sending requests to main instance")

        # stop and remove containers from possible previous runs
        print("\tStopping and removing containers from previous run ...")
        stopAndRemoveInstance(mainInstanceName)
        stopAndRemoveInstance(forwardingInstance1Name)
        stopAndRemoveInstance(forwardingInstance2Name)

        #run instances
        print("\tRunning instances ...")
        runMainInstance(hostPortMainInstance, ipAddressMainInstance, subnetName, mainInstanceName)
        runForwardingInstance(hostPortForwarding1Instance, ipAddressForwarding1Instance, subnetName, forwardingInstance1Name, ipAddressMainInstance + ":8080" )
        runForwardingInstance(hostPortForwarding2Instance, ipAddressForwarding2Instance, subnetName, forwardingInstance2Name, ipAddressMainInstance + ":8080")

        time.sleep(10)
        baseUrl = 'http://localhost:' + hostPortMainInstance

        print("\tSending requests ...")
        self.send_all_requests(baseUrl)


    def test_b_all_running_request_forwarding1(self):
        print("\nRunning all instances and sending requests to the first forwarding instance")

        # stop and remove containers from possible previous runs
        print("\tStopping and removing containers from previous run ...")
        stopAndRemoveInstance(mainInstanceName)
        stopAndRemoveInstance(forwardingInstance1Name)
        stopAndRemoveInstance(forwardingInstance2Name)

        # run instances
        print("\tRunning instances ...")
        runMainInstance(hostPortMainInstance, ipAddressMainInstance, subnetName, mainInstanceName)
        runForwardingInstance(hostPortForwarding1Instance, ipAddressForwarding1Instance, subnetName, forwardingInstance1Name, ipAddressMainInstance + ":8080" )
        runForwardingInstance(hostPortForwarding2Instance, ipAddressForwarding2Instance, subnetName, forwardingInstance2Name, ipAddressMainInstance + ":8080" )

        time.sleep(10)
        baseUrl = 'http://localhost:' + hostPortForwarding1Instance

        print("\tSending requests ...")
        self.send_all_requests(baseUrl)

    def test_c_all_running_request_forwarding2(self):
        print("\nRunning all instances and sending requests to the second forwarding instance")

        # stop and remove containers from possible previous runs
        print("\tStopping and removing containers from previous run ...")
        stopAndRemoveInstance(mainInstanceName)
        stopAndRemoveInstance(forwardingInstance1Name)
        stopAndRemoveInstance(forwardingInstance2Name)

        # run instances
        print("\tRunning instances ...")
        runMainInstance(hostPortMainInstance, ipAddressMainInstance, subnetName, mainInstanceName)
        runForwardingInstance(hostPortForwarding1Instance, ipAddressForwarding1Instance, subnetName, forwardingInstance1Name, ipAddressMainInstance + ":8080")
        runForwardingInstance(hostPortForwarding2Instance, ipAddressForwarding2Instance, subnetName, forwardingInstance2Name, ipAddressMainInstance + ":8080")

        time.sleep(10)
        baseUrl = 'http://localhost:' + hostPortForwarding2Instance

        print("\tSending requests ...")
        self.send_all_requests(baseUrl)

    def test_d_all_running_request_forwarding12(self):
        print("\nRunning all instances and sending requests to both forwarding instances")

        # stop and remove containers from possible previous runs
        print("\tStopping and removing containers from previous run ...")
        stopAndRemoveInstance(mainInstanceName)
        stopAndRemoveInstance(forwardingInstance1Name)
        stopAndRemoveInstance(forwardingInstance2Name)

        # run instances
        print("\tRunning instances ...")
        runMainInstance(hostPortMainInstance, ipAddressMainInstance, subnetName, mainInstanceName)
        runForwardingInstance(hostPortForwarding1Instance, ipAddressForwarding1Instance, subnetName, forwardingInstance1Name, ipAddressMainInstance + ":8080" )
        runForwardingInstance(hostPortForwarding2Instance, ipAddressForwarding2Instance, subnetName, forwardingInstance2Name, ipAddressMainInstance + ":8080" )

        time.sleep(10)

        print("\tSending requests ...")

        baseUrl1 = 'http://localhost:' + hostPortForwarding1Instance
        baseUrl2 = 'http://localhost:' + hostPortForwarding2Instance

        print("\tSending requests ...")
        self.send_forwarding12_requests(baseUrl1, baseUrl2)

    def test_e_main_stopped_request_forwarding12(self):

        print("\nRunning only forwarding instances (main instance is stopped) and sending requests to forwarding instances")

        # stop and remove containers from possible previous runs
        print("\tStopping and removing containers from previous run ...")
        stopAndRemoveInstance(mainInstanceName)
        stopAndRemoveInstance(forwardingInstance1Name)
        stopAndRemoveInstance(forwardingInstance2Name)

        # run instances
        print("\tRunning forwarding instances ...")
        runForwardingInstance(hostPortForwarding1Instance, ipAddressForwarding1Instance, subnetName, forwardingInstance1Name, ipAddressMainInstance + ":8080" )
        runForwardingInstance(hostPortForwarding2Instance, ipAddressForwarding2Instance, subnetName, forwardingInstance2Name, ipAddressMainInstance + ":8080")

        time.sleep(10)

        baseUrl1 = 'http://localhost:' + hostPortForwarding1Instance
        baseUrl2 = 'http://localhost:' + hostPortForwarding2Instance

        print("\tSending requests ...")
        self.send_requests_forwarding_while_main_stopped(baseUrl1)
        self.send_requests_forwarding_while_main_stopped(baseUrl2)


if __name__ == '__main__':
    unittest.main()
