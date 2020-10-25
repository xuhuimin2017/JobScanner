/* eslint-disable camelcase */
export interface JobData {
  name: string
  company: string
  company_url: string
  location: string
  type: string
  description: string | [string]
  skills: [string],
  availability: [string],
  pay_rate: string,
  experience_levels: string,
  created_at: string
}

export interface RecommendationModel {
  mySkills: [string],
  jobs: [JobData]
}
