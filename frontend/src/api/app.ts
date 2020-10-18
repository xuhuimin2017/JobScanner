import AWS from 'aws-sdk'
import { v4 as uuidV4 } from 'uuid'
import { bucketRegion, identityPoolId, bucketName, bucketPath, jobFunctionAPIBase } from 'src/api/config'
import axios from 'axios'
import { JobData } from 'components/models'

AWS.config.update({
  region: bucketRegion,
  credentials: new AWS.CognitoIdentityCredentials({
    IdentityPoolId: identityPoolId
  })
})

const _s3 = new AWS.S3({
  apiVersion: '2006-03-01',
  params: { Bucket: bucketName }
})

export function uploadResume (file: File | null): Promise<string> {
  if (!file) throw new Error('no file')
  // var fileName = file.name;
  const fileId = uuidV4()
  const fileFullKey = bucketPath + '/' + fileId

  const _upload = _s3.upload({
    Bucket: bucketName,
    Key: fileFullKey,
    Body: file
  })

  return _upload.promise().then(
    data => {
      console.log('upload done', data)
      return fileId
    },
    err => {
      throw err
    }
  )
}

export function getJobsFromResume (fileId: string) {
  return axios.get(
    `${jobFunctionAPIBase}/jobsRecommends?resume_file_id=${fileId}`,
    {
      headers: {
        // 'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      }
    }).then(
    (respData): JobData => {
      console.log('getJobsFromResume resp', respData)
      // eslint-disable-next-line @typescript-eslint/no-unsafe-return
      return respData.data
    }
  )
}
