// https://joycehong0524.medium.com/simple-android-chatting-app-using-socket-io-all-source-code-provided-7b06bc7b5aff
// https://medium.com/@raj_36650/integrate-socket-io-with-node-js-express-2292ca13d891
const SERVER_PORT = 5170

const app = require('express')()
const server = require('http').Server(app)
const io = require('socket.io')(server)

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

  socket.on('newMessage', (data) => {
    console.log('newMessage triggered')

    const messageData = JSON.parse(data)
    console.log(messageData)
  })
})

const message = {
  value: 0.0,
  message: "hello",
  type: "String"
}

// ROS-NODEJS
if (process.env.ROS_DISTRO == "melodic") {
  const rosnodejs = require('rosnodejs')

  rosnodejs.initNode('/my_node')
    .then(() => {
      // do stuff
    });

  const nh = rosnodejs.nh
  const sub = nh.subscribe('/mockSensor', 'std_msgs/Float32', (msg) => {
    console.log('Got msg on chatter: %j', msg)
    message.value = msg.data
    io.sockets.emit('robot-message', message)
  });

  // const pub = nh.advertise('/chatter', 'std_msgs/String')
  // setInterval(() => {
  //   console.log("publishing")
  //   pub.publish({ data: "hi from nodejs" })
  // }, 1000)
}