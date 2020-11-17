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
              <q-badge :color="isSkillIncomeIncrease ? 'green' : 'red'" align="top">
                {{ (isSkillIncomeIncrease ? '↑' : '↓') }} ${{ Math.floor(lastIncomeVal - mock.originalIncome) }}
              </q-badge>
            </div>
          </div>
        </q-item-section>
      </q-item>

      <q-item-label header>
        <div class="row no-wrap justify-between items-center">
          <div>Your highlight skills</div>
          <template v-if="!briefView">
            <q-btn v-if="!skillEditing" rounded dense flat color="primary" @click="skillEditing = true">
              <q-icon name="mdi-cog" class="q-mr-sm rotating"></q-icon>
              Build your skills!
            </q-btn>
            <q-btn v-else label="Reset" rounded dense flat color="primary" icon="mdi-refresh"
                   @click="skillEditing = false; onBuildReset()">
            </q-btn>
          </template>
        </div>
      </q-item-label>

      <q-item>
        <q-item-section>
          <q-item-label :lines="briefView ? 1 : 0">
            <div class="row no-wrap q-gutter-lg skill-editor items-stretch" :class="{ skillEditing }">
              <div class="multiline-tag" :class="{ 'col-6': skillEditing }">
                <drop-list
                  :items="skillSelected"
                  mode="cut"
                  @insert="onInsertSkill(skillSelected, $event)"
                  class="draggable-container full-height"
                  @reorder="$event.apply(skillSelected)"
                >
                  <template v-slot:item="{item}">
                    <drag class="draggable" :key="item" :data="item" @cut="removeSkill(skillSelected, item)">
                      <q-badge
                        class="skill-tag q-mr-xs"
                        text-color="white"
                        :color="mySkills.includes(item) ? 'primary' : 'orange'">{{ item }}</q-badge>
                    </drag>
                  </template>
                  <template v-slot:feedback="{data}">
                    <div class="draggable feedback" :key="data">
                      <q-badge
                        class="skill-tag q-mr-xs"
                        text-color="white"
                        outline
                        :color="mySkills.includes(data) ? 'primary' : 'orange'">{{ data }}</q-badge>
                    </div>
                  </template>
                </drop-list>
              </div>

              <div class="multiline-tag" v-if="skillEditing && !briefView">
                <drop-list
                  :items="mock.skillPool"
                  mode="cut"
                  class="draggable-container full-height"
                  @insert="onInsertSkill(mock.skillPool, $event)"
                  @reorder="$event.apply(mock.skillPool)"
                >
                  <template v-slot:item="{item}">
                    <drag class="draggable" :key="item" :data="item" @cut="removeSkill(mock.skillPool, item)">
                      <q-badge
                        class="skill-tag q-mr-xs"
                        text-color="white"
                        :color="mySkills.includes(item) ? 'primary' : 'orange'">{{ item }}</q-badge>
                    </drag>
                  </template>
                  <template v-slot:feedback="{data}">
                    <div class="draggable feedback" :key="data">
                      <q-badge
                        class="skill-tag q-mr-xs"
                        text-color="white"
                        outline
                        :color="mySkills.includes(data) ? 'primary' : 'orange'">{{ data }}</q-badge>
                    </div>
                  </template>
                </drop-list>
              </div>
            </div>
          </q-item-label>
        </q-item-section>
      </q-item>

      <q-item-label header>Top recommendations</q-item-label>

      <div v-for="(job, idx) in jobDataList" :key="idx">
        <q-item
          clickable
          @click="cmdSelect(idx)"
          :active="selectedIndex===idx"
          active-class="select-highlight"
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
import countTo from 'vue-count-to'
import { Drag, DropList } from 'vue-easy-dnd'
import { clone } from 'lodash'

@Component({
  components: {
    countTo, // eslint-disable-line @typescript-eslint/no-unsafe-assignment
    Drag, // eslint-disable-line @typescript-eslint/no-unsafe-assignment
    DropList // eslint-disable-line @typescript-eslint/no-unsafe-assignment
  }
})
export default class ListingView extends Vue {
  @Prop({ type: Array, required: true }) readonly jobDataList!: [JobData];
  @Prop({ type: Array }) readonly mySkills?: [string];
  @Prop({ type: Boolean, default: false }) readonly briefView?: boolean;
  @Prop({ type: Number, default: null }) readonly selectedIndex?: number;

  get dragOptions () {
    return {
      animation: 200,
      group: 'skill',
      disabled: false
    }
  }

  mock = {
    income: 0,
    originalIncome: 0,
    skillPool: ['APIs', 'Python', 'Azure', 'TensorFlow', 'C++', 'AutoCAD', 'Internet']
  };

  mounted () {
    this.$set(this, 'skillSelected', clone(this.mySkills))
    this.onEditSkill()
    this.mock.originalIncome = this.mock.income
  }

  skillEditing = false
  skillSelected = []
  drag = false
  lastIncomeVal = 0

  get isSkillIncomeIncrease () {
    return this.lastIncomeVal - this.mock.originalIncome > 0
  }

  onBuildReset () {
    this.mock.income = this.mock.originalIncome
  }

  onInsertSkill<T> (list: Array<T>, event: {index, data}) {
    list.splice(event.index, 0, event.data)
  }

  removeSkill<T> (list: Array<T>, obj: T) {
    const index = list.indexOf(obj)
    list.splice(index, 1)
  }

  onEditSkill () {
    this.lastIncomeVal = this.mock.income
    this.mock.income = this.skillSelected.length * 110 + 90000
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

@keyframes rotation {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(359deg);
  }
}
</style>

<style lang="scss" scoped>
.skill-tag {
  margin-top: 0.2em;
  &:hover {
    //transform: scale(1.02);
    opacity: 0.9;
  }
}

.multiline-tag {
  //line-height: 1.3em !important;
}

.skillEditing {
  .draggable-container {
    padding: 1em;
    border: 0.5em dashed #c3c3ff66;
  }
  .skill-tag {
    margin-bottom: 0.4em;
    animation: swaggering 250ms infinite;
    animation-timing-function: ease-in-out;
  }
}

.skill-editor {}

.draggable-container {
  border: 0 dashed #c3c3ff66;
  transition: all 700ms;
}

.draggable {
  display: inline-flex;
  flex-direction: column;
}

$m: 0.3px;
$q: 1.8deg;
@keyframes swaggering {
  0% {
    transform: rotateZ(0) translateY(0) translateX(0);
  }
  33% {
    transform: rotateZ($q) translateY($m) translateX(-$m);
  }
  66% {
    transform: rotateZ(-$q) translateY(-$m) translateX($m);
  }
  100% {
    transform: rotateZ(0) translateY(0) translateX(0);
  }
}
</style>
