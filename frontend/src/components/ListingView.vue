<template>
  <div
    :class="{'brief-view': briefView}"
    class="list-container q-py-sm">
    <div class="q-pa-md text-h6 text-primary">
      <span v-if="briefView">
        Your list
      </span>
      <span v-else>
        Hey, we have found some jobs you may fit in!
      </span>
    </div>

    <q-separator></q-separator>
    <q-list class="rounded-borders" :dense="briefView">

      <q-item-label header>Your projected income</q-item-label>
      <q-item>
        <q-item-section>
          <div class="income-area">
            <div
              class="income-text absolute-center"
              :class="{
                'text-green': isSkillIncomeIncrease,
                'text-red': !isSkillIncomeIncrease,
              }"
            >
              <count-to
                :start-val='lastIncomeVal'
                :end-val='mock.income'
                :duration='1000'
                :decimals='2'
                prefix='$ '
                :autoplay=true>
              </count-to>
              <q-badge :color="isSkillIncomeIncrease ? 'green' : 'red'" align="top" v-if="!briefView">
                {{ (isSkillIncomeIncrease ? '↑' : '↓') }} ${{ Math.floor(lastIncomeVal - mock.originalIncome) }}
              </q-badge>
            </div>
          </div>
        </q-item-section>
      </q-item>

      <q-item-label header>
        <div class="row no-wrap items-baseline justify-between items-center">
          <div v-if="skillEditing">Skill Editor</div>
          <div v-else>{{ briefView ? 'Your skills' : 'Your highlight skills' }}</div>
          <div class="content-end" v-if="!briefView">
            <transition
              appear
              mode="out-in"
              enter-active-class="animated fadeInRight"
              leave-active-class="animated fadeOutRight"
            >
              <q-btn v-if="!skillEditing" class="btn-edit" key="btn-1" rounded dense flat color="primary" @click="skillEditing = true">
                <q-icon name="mdi-cog" class="q-mr-sm rotating"></q-icon>
                Build your skills!
              </q-btn>
              <q-btn
                v-else
                key="btn-2"
                label="Done"
                icon="mdi-check"
                rounded
                dense
                flat
                color="primary"
                @click="skillEditing = false; onBuildReset()"
              ></q-btn>
            </transition>
          </div>
        </div>
      </q-item-label>

      <q-item>
        <q-item-section>
          <q-item-label :lines="briefView ? 1 : 0">
            <skill-editor
              :skills="mySkills"
              :skills-pool="mock.skillPool"
              :brief-view="briefView"
              :in-editing="skillEditing"
              @update="onSkillEdit"
            ></skill-editor>
          </q-item-label>
        </q-item-section>
      </q-item>

      <q-item-label header>Top recommendations</q-item-label>

      <div class="relative-position">
        <div v-for="(job, idx) in jobDataList" :key="idx">
          <q-item
            clickable
            @click="cmdSelect(idx)"
            :active="selectedIndex===idx"
            active-class="select-highlight"
            :disable="skillEditing"
          >
            <q-item-section avatar>
              <q-avatar rounded color="secondary">
                {{ getNamedIcon(job) }}
              </q-avatar>
            </q-item-section>

            <template v-if="!briefView">
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
                <q-item-label caption lines="2">
                  {{ getDescription(job) }}
                </q-item-label>
                <q-item-label lines="1">
                  <q-badge color="primary" text-color="white" class="q-mr-xs" v-for="s in job.skills" :key="s">
                    {{ s }}
                  </q-badge>
                </q-item-label>
              </q-item-section>
            </template>

            <template v-else>
              <q-item-section top>
                <q-item-label lines="1" class="text-weight-medium">{{ job.name }}</q-item-label>
                <q-item-label lines="1" class="text-weight-light">{{ job.type }}</q-item-label>
                <q-item-label lines="1">{{ job.company }}</q-item-label>
              </q-item-section>
            </template>

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
          <q-separator v-if="idx !== jobDataList.length - 1" :spaced="briefView?null:'sm'" />
        </div>

        <q-inner-loading :showing="skillEditing">
          <q-spinner-gears size="50px" color="primary"  />
        </q-inner-loading>
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
import SkillEditor from 'components/SkillEditor.vue'
import { formatDescription, getNamedIcon } from 'components/processing'
import countTo from 'vue-count-to'

@Component({
  components: {
    SkillEditor,
    countTo // eslint-disable-line @typescript-eslint/no-unsafe-assignment
  }
})
export default class ListingView extends Vue {
  @Prop({ type: Array, required: true }) readonly jobDataList!: [JobData];
  @Prop({ type: Array }) readonly mySkills?: [string];
  @Prop({ type: Boolean, default: false }) readonly briefView?: boolean;
  @Prop({ type: Number, default: null }) readonly selectedIndex?: number;

  mock = {
    income: 0,
    originalIncome: 0,
    skillPool: [
      { name: 'MongoDB', type: '1' },
      { name: 'PostgreSQL', type: '1' },
      { name: 'Postman', type: '1' },
      { name: 'CloudFlare', type: '1' },
      { name: 'Google Drive Drive', type: '1' },
      { name: 'Ubuntu', type: '1' },
      { name: 'AngularJS', type: '1' },

      { name: 'jQuery', type: '2' },
      { name: 'Git', type: '2' },
      { name: 'PHP', type: '2' },
      { name: 'HTML5', type: '2' },
      { name: 'NGINX', type: '2' },
      { name: 'Slack', type: '2' },
      { name: 'JavaScript', type: '2' },

      { name: 'Sass', type: '3' },
      { name: 'Google', type: '3' },
      { name: 'IntelliJ', type: '3' },
      { name: 'Webpack', type: '3' },
      { name: 'Elasticsearch', type: '3' },
      { name: 'Ruby', type: '3' },
      { name: 'VirtualBox', type: '3' }
    ]
  };

  mounted () {
    this.onSkillEdit(this.mySkills || [])
    this.mock.originalIncome = this.mock.income
  }

  skillEditing = false
  lastIncomeVal = 0

  get isSkillIncomeIncrease () {
    return this.lastIncomeVal - this.mock.originalIncome > 0
  }

  onBuildReset () {
    this.mock.income = this.mock.originalIncome
  }

  onSkillEdit (skillSelected: [string] | []) {
    this.lastIncomeVal = this.mock.income
    this.mock.income = skillSelected.length * 110 + 90000
  }

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
  width: 100%;
  transition: all 400ms;

  &.brief-view{
    width: 20em;
  }
}

.income-text {
  font-size: xx-large;
}

.income-area {
  height: 5em;
}

.brief-view {
  .income-text {
    font-size: large;
  }
  .income-area {
    height: 3em;
  }
}

.rotating {
  animation: rotation 4s infinite linear
}

.btn-edit:hover .rotating {
  animation-duration: 2s;
}

@keyframes rotation {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(359deg);
  }
}
</style>
