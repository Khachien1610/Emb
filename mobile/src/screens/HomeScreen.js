import React, { useState, useEffect } from 'react'
import { Text, View, StyleSheet } from 'react-native'
import Ionicons from 'react-native-vector-icons/Ionicons'
import Button from '../components/Button'

import SelectDropdown from 'react-native-select-dropdown'

import axios from 'axios'

export default function HomeScreen({ navigation }) {
  const [color, setColor] = useState('#F00')
  const [notification, setNotification] = useState('Phòng đang khóa')
  const [floors, setFloors] = useState([])
  const [rooms, setRooms] = useState([])
  const [selected, setSelected] = useState(false)
  const [infoSelected, setInfoSelected] = useState({})

  const open = () => {
    let data = { ...infoSelected, active: true }
    delete data.floor
    axios
      .post('https://embedded-hust.herokuapp.com/api/servos/on', data)
      .then((res) => {
        setColor('#0F0')
        setNotification('Phòng đã được mở khóa')
      })
      .catch((err) => console.log(err))
  }

  const close = () => {
    let data = { ...infoSelected, active: false }
    delete data.floor
    axios
      .post('https://embedded-hust.herokuapp.com/api/servos/off', data)
      .then((res) => {
        setColor('#F00')
        setNotification('Phòng đã bị khóa')
      })
      .catch((err) => console.log(err))
  }

  useEffect(() => {
    const getFloors = () => {
      axios
        .get(`https://embedded-hust.herokuapp.com/api/pis`)
        .then((res) => {
          setFloors(res.data.data)
        })
        .catch((err) => console.log(err))
    }
    getFloors()
  }, [])

  const renderDropdownIcon = () => {
    return <Ionicons name="chevron-down-outline" style={styles.iconDropdown} />
  }

  return (
    <View
      style={{
        flex: 1,
      }}
    >
      {/* Dropdown */}
      <View style={styles.layoutDropdown}>
        <SelectDropdown
          data={floors}
          defaultButtonText={floors.length === 0 ? 'No floor' : 'Chọn tầng'}
          disabled={floors.length === 0 ? 1 : 0}
          buttonStyle={styles.buttonStyle}
          buttonTextStyle={styles.buttonTextStyle}
          renderDropdownIcon={renderDropdownIcon}
          dropdownIconPosition="right"
          onSelect={(item, index) => {
            setInfoSelected({ serial: item.serial, floor: item.floor })
            setRooms(item.rooms)
          }}
          buttonTextAfterSelection={(item, index) => {
            return 'Tầng ' + item.floor
          }}
          rowTextForSelection={(item, index) => {
            return 'Tầng ' + item.floor
          }}
        />
        <SelectDropdown
          data={rooms}
          defaultButtonText={rooms.length === 0 ? 'No room' : 'Chọn phòng'}
          disabled={rooms.length === 0 ? 1 : 0}
          buttonStyle={styles.buttonStyle}
          buttonTextStyle={styles.buttonTextStyle}
          renderDropdownIcon={renderDropdownIcon}
          dropdownIconPosition="right"
          onSelect={(item, index) => {
            setInfoSelected({ ...infoSelected, room: item })
            setSelected(true)
          }}
          buttonTextAfterSelection={(item, index) => {
            return `P${item}`
          }}
          rowTextForSelection={(item, index) => {
            return `P${item}`
          }}
        />
      </View>

      {!selected && (
        <View
          style={{
            flex: 1,
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          <Text style={styles.textNote}>Chọn tầng và phòng để tiếp tục...</Text>
        </View>
      )}

      {selected && (
        <View
          style={{
            flex: 0.5,
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          <Text style={styles.textHead}>
            Tầng {infoSelected.floor} - Phòng {infoSelected.room}
          </Text>
          <Ionicons name="key" style={styles.icon} color={color} />
          <Text style={styles.text}>{notification}</Text>
        </View>
      )}
      {selected && (
        <View
          style={{
            flex: 0.5,
            flexDirection: 'row',
            justifyContent: 'space-around',
            alignItems: 'center',
          }}
        >
          <Button mode="outlined" style={styles.button} onPress={open}>
            <Text style={styles.textBtn}>Mở</Text>
          </Button>
          <Button mode="outlined" style={styles.button} onPress={close}>
            <Text style={styles.textBtn}>Đóng</Text>
          </Button>
        </View>
      )}
    </View>
  )
}
const styles = StyleSheet.create({
  icon: {
    fontSize: 150,
  },
  button: {
    width: '40%',
    borderRadius: '20%',
  },
  textBtn: {
    fontSize: 20,
  },
  text: {
    fontSize: 20,
    marginTop: 15,
    color: '#424245',
  },
  textHead: {
    fontSize: 20,
    color: '#424245',
    fontWeight: 'bold',
    marginBottom: 15,
  },
  buttonStyle: {
    backgroundColor: 'white',
    borderRadius: '10%',
    borderWidth: 1,
    width: '40%',
  },
  layoutDropdown: {
    marginTop: 10,
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  buttonTextStyle: {
    color: '#424245',
  },
  iconDropdown: {
    color: '#424245',
    fontSize: 18,
  },
  textNote: {
    color: '#424245',
    fontSize: 20,
  },
})
