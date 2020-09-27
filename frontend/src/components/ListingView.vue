<template>
  <div class="column items-center">
    <q-card bordered class="q-ma-lg q-py-sm list-container">
      <div class="q-pa-md text-h6 text-primary">
        Hey, we might have found some jobs you may fit in!
      </div>
      <q-list bordered class="rounded-borders">
        <q-item-label header>Top recommendations</q-item-label>

        <div v-for="(job, idx) in jobDataList" :key="idx">
          <q-item clickable @click="cmdSelect(idx)">
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
              <q-item-label caption lines="2">{{ getDescription(job) }}</q-item-label>
              <q-item-label lines="1">
                <q-badge color="primary" text-color="white" class="q-mr-xs" v-for="s in job.skills">{{ s }}</q-badge>
              </q-item-label>
            </q-item-section>

            <q-item-section top side>
              <div class="text-grey-8 q-gutter-xs">
                <q-btn
                  class="gt-xs" size="12px" flat dense round icon="mdi-star-outline"
                  disable
                  @click.stop=""
                />
              </div>
            </q-item-section>
          </q-item>

          <!-- Not showing the separator for the last one -->
          <q-separator v-if="idx !== jobDataList.length - 1" spaced />
        </div>

      </q-list>

      <div class="column items-center q-mt-sm">
        <q-btn rounded flat color="primary" label="Start Over"></q-btn>
      </div>
    </q-card>
  </div>
</template>

<script lang="ts">
import {Vue, Component, Prop} from 'vue-property-decorator'
import {JobData} from "components/models";
import {formatDescription, getNamedIcon} from "components/processing";
// import sampleList from './sample.json'
// console.log(sampleList)

@Component
export default class ListingView extends Vue {
  @Prop({ type: Array, required: true }) readonly jobDataList!: [JobData];

  getNamedIcon(job: JobData) {
    return getNamedIcon(job)
  }

  getDescription(job: JobData) {
    return formatDescription(job)
  }

  cmdSelect(idx) {
    this.$emit('select', idx)
  }
}
</script>

<style lang="scss" scoped>
.list-container {
  width: 70vw;
  max-width: 50em;
  border-radius: 1.75em;
  box-shadow: 0px 13px 20px 2px #c3c3c34d;
}
</style>
