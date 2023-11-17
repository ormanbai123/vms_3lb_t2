import 'react-native-gesture-handler';
import * as React from 'react';
import { Platform, Text, View, StyleSheet, TextInput, TouchableOpacity, Button } from 'react-native';
import { createDrawerNavigator } from '@react-navigation/drawer';
import { NavigationContainer } from '@react-navigation/native';
import MapView, { Marker, PROVIDER_GOOGLE } from 'react-native-maps';
import { useState, useEffect } from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import Geolocation from '@react-native-community/geolocation';

var userInfo = {
  "username" : "",
  "password" : "",
  "first_name": "",
  "last_name" :"",
  "email" :""
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
        </MapView>
    </View>
    // <MapView
    //   style={{ flex: 1 }}
    //   initialRegion={{
    //     latitude: 37.78825,
    //     longitude: -122.4324,
    //     latitudeDelta: 0.0922,
    //     longitudeDelta: 0.0421,
    //   }}/>
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

function Logout({ navigation }) {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
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
        ()=>{
          navigation.navigate('LoginScreen');
        }
      }>
      </Button>
    </View>
  );
}

function Tasks({ navigation }){
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
    <Text> {userInfo.username} </Text>
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
// Change useLegacyImplementation parameter in future!
function Body() {
  return (
      <Drawer.Navigator initialRouteName="Home">
        <Drawer.Screen name="Home" component={HomeScreen} />
        <Drawer.Screen name="Tasks" component={Tasks} />
        <Drawer.Screen name="History" component={History} />
        <Drawer.Screen name="Logout" component={Logout} />
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
        <Stack.Screen name="LoginScreen" component={LoginScreen} />
        <Stack.Screen name="Body" component={Body} options={{
          headerShown: false
        }} />
      </Stack.Navigator>
    </NavigationContainer>
  )
}

