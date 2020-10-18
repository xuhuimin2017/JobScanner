import { JobData } from 'components/models'

export const getNamedIcon = function (job: JobData) {
  return job.company?.trim().substr(0, 1)
}

export const formatDescription = function (job: JobData) {
  return typeof job.description === 'object' ? job.description.join(' ') : job.description
}
