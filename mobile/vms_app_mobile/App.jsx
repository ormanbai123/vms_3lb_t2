import 'react-native-gesture-handler';
import * as React from 'react';
import { Platform, Text, View, StyleSheet, TextInput, TouchableOpacity, Button } from 'react-native';
import { createDrawerNavigator } from '@react-navigation/drawer';
import { NavigationContainer } from '@react-navigation/native';
import MapView, { Marker, PROVIDER_GOOGLE } from 'react-native-maps';
import MapViewDirections from 'react-native-maps-directions';
import { useState, useEffect, useRef } from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import Geolocation from '@react-native-community/geolocation';
import { FlatList } from 'react-native-gesture-handler';

var userInfo = {
  "username" : "",
  "password" : "",
  "first_name": "",
  "last_name" :"",
  "email" :"",
  "government_id":"",
  "driving_license_code":"",
  "phone_number":"",
};

var userTasks = [
    { id: '1', pointA: 'Item 1', pointB: 'Item 1', date: "21" },
    { id: '2', pointA: 'Item 2', pointB: 'Item 2', date: "20" },
    { id: '3', pointA: 'Item 3', pointB: 'Item 3', date: "19" },
    { id: '4', pointA: 'Item 4', pointB: 'Item 4', date: "18" },
    { id: '5', pointA: 'Item 5', pointB: 'Item 5', date: "17" },
    { id: '6', pointA: 'Item 6', pointB: 'Item 6', date: "16" },
];

const latitudeDelta =  0.005;
const longitudeDelta =  0.005;


const MapStyles = StyleSheet.create({
  container: {
    ...StyleSheet.absoluteFillObject,
    flex: 1, //the container will fill the whole screen.
    justifyContent: "flex-end",
    alignItems: "center",
  },
  map: {
    ...StyleSheet.absoluteFillObject,
  },
});

const Drawer = createDrawerNavigator();
function Body() {
    const [driverActive, setDriverActive] = useState(false);
    const [taskList, setTaskList] = useState(userTasks)

    function HomeScreen({ navigation }) {
        const [currentLatitude, setCurrentLatitude] = useState(51.090108);
        const [currentLongitude, setCurrentLongitude] = useState(71.399909);
        const mapRef = useRef();

        useEffect(() => {
          Geolocation.getCurrentPosition(
            (position)=>{
                setCurrentLatitude(position.coords.latitude);
                setCurrentLongitude(position.coords.longitude);
                console.log(currentLatitude, currentLongitude);
            },
            (error)=>{
              console.error(error.message);
              return;
            },
            { enableHighAccuracy: true, timeout: 20000, maximumAge: 10000 }
          );

          // Set up location updates
          const watchId = Geolocation.watchPosition(
            (position) => {
              const { latitude, longitude } = position.coords;
              setCurrentLatitude(latitude);
              setCurrentLongitude(longitude);
            },
            (error) => console.error(error),
            { enableHighAccuracy: true, timeout: 20000, maximumAge: 10000, distanceFilter: 10 }
          );

          return () => {
            // Clear watch when the component unmounts
            Geolocation.clearWatch(watchId);
          };
        }, []);

        return (
          <View style={MapStyles.container}>
              <MapView style={MapStyles.map} initialRegion={{
                latitude : currentLatitude,
                longitude : currentLongitude,
                latitudeDelta : latitudeDelta,
                longitudeDelta : longitudeDelta,
              }}
               provider={PROVIDER_GOOGLE}
               ref={mapRef}
               region={
                {
                  latitude:currentLatitude,
                  longitude:currentLongitude,
                  longitudeDelta: longitudeDelta,
                  latitudeDelta:latitudeDelta
                }
               }
               >
                <Marker coordinate={{latitude:currentLatitude, longitude:currentLongitude}}>
                </Marker>

                <MapViewDirections
                 origin={{latitude:currentLatitude, longitude:currentLongitude}}
                 destination={{latitude:currentLatitude+0.5, longitude:currentLongitude+0.5}}
                 apikey='AIzaSyBvAYRE_P_EDKwm6bx92F0mKh49LYfr2X0'
                 strokeWidth={3}
                 strokeColor='hotpink'
                 />

              </MapView>
              
      
              <View
                style={{
                    position: 'absolute',//use absolute position to show button on top of the map
                    bottom: '1%', //for center align
                    //left: '50%',
                    right: '50%',
                }}>
                  { driverActive  && <Button title='End route' onPress={()=>{
                    setDriverActive(false);
                  }} />}
              </View>
      
          </View>
        );
      }
        

    function History({ navigation }){
    return (
        <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        <Text> {userInfo.email} </Text>
        </View>
    );
    }

    function Tasks({ navigation }){
        const handleAccept = (itemId) => {
          const updatedTaskList = taskList.filter((item) => item.id !== itemId);
          setTaskList(updatedTaskList);
          setDriverActive(true);
          navigation.navigate('Home');
        };
        const handleReject = (itemId) => {
          // Implement reject logic if needed
          // For example, you can remove the rejected item from the list
        };

        const renderItem = ({ item }) => (
          <View style={{marginHorizontal:8,
            marginVertical:16,
            padding:20}}>
            <Text>{"\n"}Date: {item.date}</Text>
            <Text>From: {item.pointA}</Text>
            <Text>To: {item.pointB}</Text>
            <View style={{flexDirection: 'row'}}>
              <Button
                title="Accept"
                onPress={() => handleAccept(item.id)}
                disabled={driverActive === true}
                color='green'
              />
              <Button
                title="Reject"
                onPress={() => handleReject(item.id)}
                disabled={driverActive === true}
                color='red'
              />
            </View>
          </View>
        );
        return (
          <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
            <FlatList 
              data={taskList}
              renderItem={renderItem}
              keyExtractor={(item) => item.id}
            />
          </View>
        );
      }
    
    function AccountInfo({ navigation }) {
        const [localUserInfo, setLocalUserInfo] = useState(userInfo);
        
        const localStyles = StyleSheet.create({
          label: {
            fontSize: 16,
            fontWeight: 'bold',
            marginBottom: 5,
          },
          field: {
            fontSize: 16,
            marginBottom: 15,
          },
        });
      
        return (
          <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
            
            <Text style={localStyles.label}>IIN:</Text>
            <Text style={localStyles.field}>{localUserInfo.government_id}</Text>
      
            <Text style={localStyles.label}>Driving license code:</Text>
            <Text style={localStyles.field}>{localUserInfo.driving_license_code}</Text>
      
            <Text style={localStyles.label}>First name:</Text>
            <Text style={localStyles.field}>{localUserInfo.first_name}</Text>
      
            <Text style={localStyles.label}>Last name:</Text>
            <Text style={localStyles.field}>{localUserInfo.last_name}</Text>
      
            <Text style={localStyles.label}>Phone number:</Text>
            <Text style={localStyles.field}>{localUserInfo.phone_number}</Text>
      
            <Text style={localStyles.label}>Username:</Text>
            <Text style={localStyles.field}>{localUserInfo.username}</Text>
      
            <Text style={localStyles.label}>Password:</Text>
            <Text style={localStyles.field}>{localUserInfo.password}</Text>
      
            <Text style={localStyles.label}>Email:</Text>
            <Text style={localStyles.field}>{localUserInfo.email}</Text>
      
            <Button title="Log out" onPress={
              //-----Production code---------------
              // async ()=>{
              //   const serverURL = "http://10.0.2.2:8000/api/logout/";
              //   try{
              //     const response = await fetch(serverURL);
              //     navigation.navigate('LoginScreen');
              //   } catch(error){
              //     console.error(error);
              //   }
              // }
              //-------------------------------------
      
              // Debug code---------------
              ()=>{
                navigation.navigate('LoginScreen');
              }
              // -------------------------------
            }>
            </Button>
          </View>
        );
    }

    return (
        <Drawer.Navigator initialRouteName="Home">
            <Drawer.Screen name="Home" component={HomeScreen} options={{headerTransparent:true}} />
            <Drawer.Screen name="Tasks" component={Tasks} />
            <Drawer.Screen name="History" component={History} />
            <Drawer.Screen name="Account Info" component={AccountInfo} />
        </Drawer.Navigator>
    );
}







const LoginScreen = ({ navigation }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    // Login functionality
    // NOTE
    // add slashes ('/') at the end of URL!
    const serverURL = "http://10.0.2.2:8000/api/login/";


    //-------------------Production---------------------------------
    // try{
    //   const response = await fetch(serverURL, {
    //     method: 'POST',
    //     headers: {
    //     "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify({
    //       'username': username,
    //       'password': password,
    //     }),
    //   });
    //   const responseMsg = await response.json();
    //   if (responseMsg.status === "success") {
    //     userInfo.username = username;
    //     userInfo.password = password;
    //     userInfo.email = responseMsg.data.email;
    //     userInfo.first_name = responseMsg.data.first_name;
    //     userInfo.last_name = responseMsg.data.last_name;
    //     userInfo.government_id = responseMsg.data.government_id
    //     userInfo.driving_license_code = responseMsg.data.driving_license_code
    //     userInfo.phone_number = responseMsg.data.phone_number
    //     navigation.navigate("Body");
    //   } else {
    //     console.error("API post request fail!");
    //   }
      
    // }catch (error){
    //   console.error(error);
    // }
    //-------------------------------------------------------------------


      //--------------When testing-------------------------
      navigation.navigate("Body")
      //--------------------------------------
    };

  return (
    <View style={LoginStyles.container}>
      <Text style={LoginStyles.title}>Login</Text>
      <TextInput
        style={LoginStyles.input}
        placeholder="Username"
        onChangeText={(text) => {
          setUsername(text);
          userInfo.username = text; }  }
        value={username}
      />
      <TextInput
        style={LoginStyles.input}
        placeholder="Password"
        secureTextEntry
        onChangeText={(text) => {
          setPassword(text);
          userInfo.password = text; } }
        value={password}
      />
      <TouchableOpacity style={LoginStyles.button} onPress={handleLogin}>
        <Text style={LoginStyles.buttonText}>Log in</Text>
      </TouchableOpacity>
    </View>
  );
};

const LoginStyles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    marginBottom: 20,
  },
  input: {
    width: '80%',
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    padding: 10,
  },
  button: {
    backgroundColor: 'blue',
    padding: 10,
    borderRadius: 5,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    textAlign: 'center',
  },
});

const Stack = createStackNavigator();


export default function Main(){
  return(
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="LoginScreen" component={LoginScreen}  options={{headerShown:false}} />
        <Stack.Screen name="Body" component={Body} options={{
          headerShown: false
        }} />
      </Stack.Navigator>
    </NavigationContainer>
  )
}

