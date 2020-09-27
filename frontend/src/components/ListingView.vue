<template>
  <div class="column items-center">
    <q-card flat bordered class="q-ma-lg q-py-sm list-container">
      <div class="q-pa-md text-h6 text-primary">
        Hey, we might have found some jobs you may fit in!
      </div>
      <q-list bordered class="rounded-borders">
        <q-item-label header>Top recommendations</q-item-label>

        <div v-for="(job, idx) in listData" :key="idx">
          <q-item clickable>
            <q-item-section avatar>
              <q-avatar rounded color="secondary">
                {{ getNamedIcon(job) }}
              </q-avatar>
            </q-item-section>

            <q-item-section top class="col-3">
              <q-item-label class="q-mt-sm">{{ job.company }}</q-item-label>
              <q-item-label lines="1">
                <span class="text-weight-thin">{{ job.location }}</span>
              </q-item-label>
            </q-item-section>

            <q-item-section top>
              <q-item-label lines="1">
                <span class="text-weight-medium">{{ job.name }}</span>
                <span class="text-grey-8"> - {{ job.type }}</span>
              </q-item-label>
              <q-item-label caption lines="2">{{ formatDescription(job) }}</q-item-label>
              <q-item-label lines="1">
                <q-badge color="primary" text-color="white" class="q-mr-xs" v-for="s in job.skills">{{ s }}</q-badge>
              </q-item-label>
            </q-item-section>

            <q-item-section top side>
              <div class="text-grey-8 q-gutter-xs">
                <q-btn class="gt-xs" size="12px" flat dense round icon="mdi-star-outline" />
              </div>
            </q-item-section>
          </q-item>

          <q-separator v-if="idx !== listData.length - 1" spaced />
        </div>

      </q-list>

      <div class="column items-center q-mt-sm">
        <q-btn rounded flat color="primary" label="Start Over"></q-btn>
      </div>
    </q-card>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import sampleList from './sample.json'
// console.log(sampleList)

@Component
export default class ListingView extends Vue {
  listData = sampleList

  getNamedIcon(job: any) {
    return job.company?.trim().substr(0, 1)
  }

  formatDescription(job: any) {
    return typeof job.description === 'object' ? job.description.join(' ') : job.description
  }
}
</script>

<style lang="scss" scoped>
.list-container {
  width: 70vw;
  max-width: 50em;
  border-radius: 1.75em;
}
</style>
