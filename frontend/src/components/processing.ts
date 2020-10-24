import { JobData } from 'components/models'

export const getNamedIcon = function (job: JobData) {
  return job.company?.trim().substr(0, 1)
}

export const formatDescription = function (job: JobData) {
  return job.description instanceof Array
    ? job.description.join(' ')
    : job.description
}
