<template>
  <div class="column items-center">
    <q-card bordered class="q-ma-lg q-py-sm list-container">

      <q-card-section class="bg-primary text-white">
        <div class="text-h6 ellipsis">
          {{ jobData.name }} -
          <span class="text-weight-light">{{ jobData.type}}</span>
          <div class="float-right" >
            <q-btn
              round flat dense icon="mdi-undo-variant"
              title="Back to list"
              @click="$emit('close')"
            ></q-btn>
            <q-btn round flat dense icon="mdi-open-in-new"></q-btn>
          </div>
        </div>
        <div class="text-subtitle2">
          <a class="text-white" :href="jobData.company_url" target="_blank">{{ jobData.company }}</a>
        </div>
        <div class="text-caption">{{ jobData.location }}</div>
      </q-card-section>

      <q-card-section class="row justify-between">
        <q-item dense>
          <q-item-section avatar>
            <q-icon name="mdi-clock-time-eight-outline"></q-icon>
          </q-item-section>
          <q-item-section>
            <q-item-label>Availability</q-item-label>
            <q-item-label caption lines="1" v-for="a in jobData.availability" :key="a">
              {{ a }}
            </q-item-label>
          </q-item-section>
        </q-item>

        <q-item dense>
          <q-item-section avatar>
            <q-icon name="mdi-cash-100"></q-icon>
          </q-item-section>
          <q-item-section>
            <q-item-label>Pay rate</q-item-label>
            <q-item-label caption lines="1">
              {{ jobData.pay_rate }}
              {{ jobData.pay_rate }}
            </q-item-label>
          </q-item-section>
        </q-item>

        <q-item>
          <q-item-section avatar>
            <q-icon name="mdi-briefcase-outline"></q-icon>
          </q-item-section>
          <q-item-section>
            <q-item-label>Experience Level</q-item-label>
            <template
              v-if="jobData.experience_levels">
              <q-item-label caption lines="1" v-for="e in jobData.experience_levels" :key="e">
                {{ e }}
              </q-item-label>
            </template>
            <q-item-label v-else>Not listed</q-item-label>
          </q-item-section>
        </q-item>
      </q-card-section>

      <q-separator inset />

      <q-card-section>
        <div class="text-body2">
          {{jobData.created_at}}
          <span class="text-weight-thin">(Updated)</span>
        </div>
      </q-card-section>

      <q-card-section>
        <div class="text-subtitle1">Job description</div>
        <div class="text-body2">{{ getDescription(jobData) }}</div>
      </q-card-section>

      <q-card-section>
        <div class="text-subtitle1">Skills</div>
        <q-badge
          color="primary"
          text-color="white"
          class="q-mr-xs"
          v-for="s in jobData.skills" :key="s">
          {{ s }}
        </q-badge>
      </q-card-section>

      <div class="row justify-between q-mt-sm">
        <q-btn
          rounded flat color="primary"
          icon="mdi-arrow-left-circle-outline"
          label="Previous">
        </q-btn>
        <q-btn
          rounded flat color="primary"
          icon-right="mdi-arrow-right-circle-outline"
          label="Next">
        </q-btn>
      </div>
    </q-card>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import { JobData } from 'components/models'

import { formatDescription } from 'components/processing'

@Component
export default class JDView extends Vue {
  @Prop({ type: Object, required: true }) readonly jobData!: JobData;

  getDescription (job: JobData) {
    return formatDescription(job)
  }
}
</script>

<style lang="scss" scoped>
.list-container {
  width: 70vw;
  max-width: 50em;
  border-radius: 1.75em;
  box-shadow: 0px 13px 20px 2px #c3c3c34d;
  border-width: 0;
}

</style>
