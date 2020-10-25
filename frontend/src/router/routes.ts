import { RouteConfig } from 'vue-router'

const routes: RouteConfig[] = [
  {
    path: '/',
    component: () => import('layouts/CardLayout.vue'),
    children: [
      // { path: 'index', component: () => import('pages/Index.vue') },
      { name: 'upload', path: '', component: () => import('pages/UploadView.vue') },
      {
        name: 'result',
        path: 'result',
        component: () => import('pages/JobPage.vue'),
        props: route => ({
          // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
          recommendationData: route.params.recommendationData && JSON.parse(route.params.recommendationData)
        })
      }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
