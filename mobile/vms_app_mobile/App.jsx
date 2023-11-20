import 'react-native-gesture-handler';
import * as React from 'react';
import { Platform, Text, View, StyleSheet, TextInput, TouchableOpacity, Button } from 'react-native';
import { createDrawerNavigator } from '@react-navigation/drawer';
import { NavigationContainer } from '@react-navigation/native';
import MapView, { Marker, PROVIDER_GOOGLE } from 'react-native-maps';
import { useState, useEffect } from 'react';
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


function HomeScreen({ navigation }) {
  
  const [currentLatitude, setCurrentLatitude] = useState(51.090108);
  const [currentLongitude, setCurrentLongitude] = useState(71.399909);
  const latitudeDelta =  0.005;
  const longitudeDelta =  0.005;

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
      { enableHighAccuracy: true, timeout: 20000, maximumAge: 1000 }
    );
  }, []);

  function regionChange(region) {
    setCurrentLatitude(region.latitude);
    setCurrentLongitude(region.longitude);
    latitudeDelta = region.latitudeDelta;
    longitudeDelta = region.longitudeDelta;
  }

  return (
    <View style={MapStyles.container}>
        <MapView style={MapStyles.map} initialRegion={{
          latitude : currentLatitude,
          longitude : currentLongitude,
          latitudeDelta : latitudeDelta,
          longitudeDelta : longitudeDelta,
        }}
         provider={PROVIDER_GOOGLE}
         //onRegionChange={regionChange} 
         >
          <Marker coordinate={{latitude:currentLatitude, longitude:currentLongitude}}>
          </Marker>
        </MapView>
        

        <View
          style={{
              position: 'absolute',//use absolute position to show button on top of the map
              bottom: '1%', //for center align
              //left: '50%',
              right: '50%',
          }}>
          <Button title='End route' />
        </View>

    </View>
  );
}


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

function Tasks({ navigation }){
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
    <FlatList 
    data={}
    renderItem={}
    extraData={}>
    </FlatList>
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

const Drawer = createDrawerNavigator();
function Body() {
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

