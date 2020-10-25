<template>
  <div
    :class="{small: small}"
    class="list-container q-py-sm">
    <div class="q-pa-md text-h6 text-primary">
      <span v-if="small">
        Your list
      </span>
      <span v-else>
        Hey, we have found some jobs you may fit in!
      </span>
    </div>

    <q-separator></q-separator>
    <q-list class="rounded-borders" :dense="small">
      <q-item-label header>Your highlight skills</q-item-label>
      <q-item>
        <q-item-section>
          <q-item-label>
            <div class="multiline-tag">
              <q-badge class="skill-tag q-mr-xs" color="primary" text-color="white" v-for="s in mySkills" :key="s">
                {{ s }}
              </q-badge>
            </div>
          </q-item-label>
        </q-item-section>
      </q-item>

      <q-item-label header>Top recommendations</q-item-label>

      <div v-for="(job, idx) in jobDataList" :key="idx">
        <q-item clickable @click="cmdSelect(idx)">
          <q-item-section avatar>
            <q-avatar rounded color="secondary">
              {{ getNamedIcon(job) }}
            </q-avatar>
          </q-item-section>

          <q-item-section top class="col-3" v-if="!small">
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
            <q-item-label caption lines="2">
              {{ getDescription(job) }}
            </q-item-label>
            <q-item-label lines="1" v-if="!small">
              <q-badge color="primary" text-color="white" class="q-mr-xs" v-for="s in job.skills" :key="s">
                {{ s }}
              </q-badge>
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
    <q-separator></q-separator>

    <div class="column items-center q-mt-sm">
      <q-btn rounded flat color="primary" label="Start Over" @click="$router.push({name: 'upload'})"></q-btn>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import { JobData } from 'components/models'
import { formatDescription, getNamedIcon } from 'components/processing'

@Component
export default class ListingView extends Vue {
  @Prop({ type: Array, required: true }) readonly jobDataList!: [JobData];
  @Prop({ type: Array }) readonly mySkills?: [string];
  @Prop({ type: Boolean }) readonly small?: boolean;

  getNamedIcon (job: JobData) {
    return getNamedIcon(job)
  }

  getDescription (job: JobData) {
    return formatDescription(job)
  }

  cmdSelect (idx: number) {
    this.$emit('select', idx)
  }
}
</script>

<style lang="scss" scoped>
.list-container {
  width: 70vw;
  max-width: 80em;
  //transition: width 500ms ease;

  &.small{
    width: 20em;
  }
}

.multiline-tag {
  line-height: 1.3em !important;
}

.skill-tag {
  transition: all 300ms;
  &:hover {
    //transform: scale(1.02);
    opacity: 0.9;
  }
}
</style>
