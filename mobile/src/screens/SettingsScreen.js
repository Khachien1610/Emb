import React, { useEffect, useState } from 'react'
import { Text, View, StyleSheet } from 'react-native'
import Button from '../components/Button'

import * as SecureStore from 'expo-secure-store'
import Ionicons from 'react-native-vector-icons/Ionicons'
import axios from 'axios'

export default function SettingsScreen({ navigation }) {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')

  useEffect(() => {
    const fetchUser = async () => {
      let info = await SecureStore.getItemAsync('info')
      let userId = JSON.parse(info).userId
      axios
        .get(`https://embedded-hust.herokuapp.com/api/users/${userId}`)
        .then((res) => {
          setUsername(res.data.data.username)
          setEmail(res.data.data.email)
        })
        .catch((err) => console.log(err))
    }
    fetchUser()
  }, [])

  const onLogOutPressed = async () => {
    await SecureStore.deleteItemAsync('info')
    navigation.reset({
      index: 0,
      routes: [{ name: 'StartScreen' }],
    })
  }
  return (
    <View style={{ flex: 1, alignItems: 'center' }}>
      <Button mode="outlined" style={[styles.button, styles.flexStart]}>
        <View style={styles.lay}>
          <View>
            <Ionicons name="person-circle-outline" style={styles.icon} />
          </View>
          <View style={{ marginLeft: 10 }}>
            <Text style={styles.blue}>Thông tin tài khoản</Text>
            <Text style={styles.gray}>{username}</Text>
            <Text style={styles.gray}>{email}</Text>
          </View>
        </View>
      </Button>
      <Button mode="outlined" style={styles.button} onPress={onLogOutPressed}>
        <Text style={styles.red}>Đăng xuất</Text>
      </Button>
    </View>
  )
}

const styles = StyleSheet.create({
  button: {
    width: '95%',
    borderRadius: '10%',
    display: 'flex',
    alignItems: 'center',
  },
  flexStart: {
    alignItems: 'flex-start',
  },
  lay: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
  },
  icon: {
    color: '#0071e3',
    fontSize: 60,
  },
  blue: {
    color: '#0071e3',
    fontWeight: 'bold',
    fontSize: 20,
  },
  red: {
    color: 'red',
    fontWeight: 'bold',
    fontSize: 20,
  },
  gray: {
    color: '#424245',
    fontSize: 16,
  },
})
