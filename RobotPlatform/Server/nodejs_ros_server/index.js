// https://joycehong0524.medium.com/simple-android-chatting-app-using-socket-io-all-source-code-provided-7b06bc7b5aff
// https://medium.com/@raj_36650/integrate-socket-io-with-node-js-express-2292ca13d891
const SERVER_PORT = 5170

const app = require('express')()
const server = require('http').Server(app)
const io = require('socket.io')(server)
const events = require('events')

var eventEmitter = new events.EventEmitter()

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html')
});

server.listen(SERVER_PORT, () => {
  console.log(`listening on *:${SERVER_PORT}`)
})

io.on('connection', (socket) => {
  console.log('A user connected')

  socket.on('disconnect', () => {
    console.log('A user disconnected')
  })

  socket.on('robot-command', (data) => {
    // console.log('robot-command triggered')

    const messageData = JSON.parse(data)
    eventEmitter.emit('joystickData', messageData)
    // console.log(messageData)
  })
})

const message = {
  velocityEncoder: 0.0
}

// ROS-NODEJS
if (process.env.ROS_DISTRO == "melodic") {
  const rosnodejs = require('rosnodejs')

  rosnodejs.initNode('/my_node')
    .then(() => {
      // do stuff
    })

  const nh = rosnodejs.nh
  const sub1 = nh.subscribe('/magnet_encoder/value', 'std_msgs/Float32', (msg) => {
    message.velocityEncoder = msg.data
    io.sockets.emit('robot-message', message)
  })

  const sub2 = nh.subscribe('/imu/mag', 'sensor_msgs/MagneticField', (msg) => {
    // message.velocityEncoder = msg.data
    // io.sockets.emit('robot-message', message)
    // console.log(msg)
  })

  const twistMessage = {
    linear : {
      x : 0.0,
      y : 0.0,
      z : 0.0
    },
    angular : {
      x : 0.0,
      y : 0.0,
      z : 0.0
    }
  }

  const pub = nh.advertise('/joy_driver/joy', 'geometry_msgs/Twist')
  eventEmitter.on('joystickData', (data) => {
    twistMessage.linear.x = data.steering
    twistMessage.angular.z = data.throttle
    // console.log(twistMessage)
    pub.publish(twistMessage)
  })

  // setInterval(() => {
  //   console.log("publishing")
  //   twistMessage.linear.x = steering
  //   pub.publish({ linear: { x = } })
  // }, 1000)
}