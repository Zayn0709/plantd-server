import * as admin from "firebase-admin"
import * as MongoClient from 'mongodb'
import { exit } from "process"

const serviceAccount = require('./firebase-service.json')

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
})

let init = async () => {
    const firestore = admin.firestore()
    const db = (await MongoClient.connect('mongodb://localhost:27017', {
        useUnifiedTopology: true
    })).db('plantd')
    const diseases = await db.collection('disease').find().toArray()
    const plants = await db.collection('plant').find().toArray()

    for (const item of plants) {
        const id = `${item['_id']}`
        delete item['_id']

        await firestore.collection('plants').doc(id).set(item)
    }

    for (const item of diseases) {
        const id = `${item['_id']}`
        delete item['_id']
        item['plantId'] = item['plantId'].toString()
        item['imgUrl'] = 'plants' + item['imgUrl'].substr(12)
        await firestore.collection('diseases').doc(id).set(item)
    }
}

console.log("BEGIN")
init().then(() => {
    console.log("FINISH")
    exit(0)
})
