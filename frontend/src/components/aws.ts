import AWS from 'aws-sdk'
import { v4 as uuidV4 } from 'uuid'

const resumeBucketName = 'jobscanner-test'
const bucketRegion = 'us-east-2'
const identityPoolId = 'us-east-2:24f7c99e-aaae-4e9c-847a-0aea505dbddb'
const uploadPath = 'resume_upload'

AWS.config.update({
  region: bucketRegion,
  credentials: new AWS.CognitoIdentityCredentials({
    IdentityPoolId: identityPoolId
  })
})

const s3 = new AWS.S3({
  apiVersion: '2006-03-01',
  params: { Bucket: resumeBucketName }
})

export function uploadResume (file: File) {
  // var fileName = file.name;
  const fileKey = uploadPath + '/' + uuidV4()

  const _upload = s3.upload({
    Bucket: resumeBucketName,
    Key: fileKey,
    Body: file
  })

  return _upload.promise().then(
    (data) => {
      console.log('upload done', data)
      return fileKey
    },
    (err) => {
      throw err
    }
  )
}
