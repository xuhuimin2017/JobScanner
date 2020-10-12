import AWS from "aws-sdk";
import { v4 as uuidV4 } from 'uuid'

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
