export interface JobData {
  name: string
  company: string
  // eslint-disable-next-line camelcase
  company_url: string
  location: string
  type: string
  description: string | [string]
  skills: [string]
}

export interface RecommendationModel {
  mySkills: [string],
  jobs: [JobData]
}
