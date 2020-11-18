<template>
  <div class="column">
    <div class="row no-wrap skill-editor items-stretch justify-around" :class="{ allowEdit }">
      <div :class="{ 'q-pr-md': allowEdit }">
        <transition
          appear
          enter-active-class="animated fadeInUp"
          leave-active-class="animated fadeOutDown"
        >
          <div
            v-if="allowEdit"
            class="area-title q-mb-sm text-weight-medium text-primary"
          >
            Yours
          </div>
        </transition>
        <drop-list
          :items="skillSelected"
          mode="cut"
          @insert="onInsertSkill(skillSelected, $event)"
          class="skill-area skill-my draggable-container full-height"
          @reorder="$event.apply(skillSelected)"
        >
          <template v-slot:item="{item}">
            <drag
              class="draggable"
              :key="item.name"
              :data="item"
              @cut="removeSkill(skillSelected, item)"
            >
              <q-badge
                class="skill-tag q-mr-xs"
                text-color="white"
                :color="skillColor(item)">
                {{ item.name }}
                <q-icon
                  v-if="allowEdit && item.type !== 'my-skill'"
                  :name="hoverClose[item.name] ? 'mdi-close-circle' : 'mdi-close-circle-outline'"
                  color="white"
                  class="q-ml-xs cursor-pointer"
                  @click.stop="removeSkill(skillSelected, item)"
                  @mousedown.stop
                  @mouseenter="$set(hoverClose, item.name, true)"
                  @mouseleave="$set(hoverClose, item.name, false)"
                />
              </q-badge>
            </drag>
          </template>
          <template v-slot:feedback="{data}">
            <div class="draggable feedback" :key="data.name">
              <q-badge
                class="skill-tag q-mr-xs"
                text-color="white"
                outline
                :color="skillColor(data)">{{ data.name }}</q-badge>
            </div>
          </template>
        </drop-list>
      </div>

      <transition
        appear
        mode="out-in"
        enter-active-class="animated fadeInRightBig"
        leave-active-class="animated fadeOutRightBig"
      >
        <div class="col-6 q-pl-md" v-if="allowEdit">
          <div class="area-title q-mb-sm text-weight-medium text-orange">
            Skill Market
          </div>
          <div class="skill-area skill-pool full-height">
            <div v-for="i in [1, 2, 3]" :key="i" class="q-mb-sm">
              <div class="text-caption">
                Skill Type {{i}}
                <q-btn
                  color="primary"
                  dense
                  flat
                  icon="mdi-autorenew"
                  class="skill-refresh-btn"
                  no-caps
                  rounded
                  size="xs"
                  title="Show more"
                  :loading="hoverSkillLoading[i]"
                  @click="$set(hoverSkillLoading, i, true)"
                ></q-btn>
              </div>
              <drag
                v-for="item in skillsPoolDirty.filter(item => item.type === String(i))"
                :key="item.name"
                :data="item"
                @cut="removeSkill(skillsPoolDirty, item)"
                class="draggable"
              >
                <q-badge
                  class="skill-tag q-mr-xs"
                  text-color="white"
                  :color="skillColor(item)">{{ item.name }}</q-badge>
              </drag>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <div class="row q-mt-xl q-gutter-sm justify-center" v-if="allowEdit">
      <!--<q-btn rounded color="primary">Looks Good!</q-btn>-->
      <q-btn rounded flat color="primary" @click="onReset">Reset</q-btn>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop, Watch } from 'vue-property-decorator'
import { Drag, DropList } from 'vue-easy-dnd'
import { clone } from 'lodash'

interface SkillType {
  name: string
  type: string
}

@Component({
  components: {
    Drag, // eslint-disable-line @typescript-eslint/no-unsafe-assignment
    DropList // eslint-disable-line @typescript-eslint/no-unsafe-assignment
  }
})
export default class SkillEditor extends Vue {
  @Prop({ type: Array }) readonly skills?: [string];
  @Prop({ type: Array }) readonly skillsPool?: [SkillType];
  @Prop({ type: Boolean, default: false }) readonly briefView?: boolean;
  @Prop({ type: Boolean, default: false }) readonly inEditing?: boolean;

  mounted () {
    this.onReset()
  }

  skillSelected: [SkillType] | [] = []
  skillsPoolDirty: [SkillType] | [] = []
  hoverClose = {}
  hoverSkillLoading = {}

  onInsertSkill<T> (list: Array<T>, event: {index: number, data: T}) {
    list.splice(event.index, 0, event.data)
  }

  removeSkill<T> (list: Array<T>, obj: T) {
    const index = list.indexOf(obj)
    list.splice(index, 1)
  }

  @Watch('skillSelected')
  updateCurrentSkill () {
    this.$emit('update', this.skillSelected)
  }

  onReset () {
    this.$set(this, 'skillSelected', clone(this.skills)?.map(i => ({ name: i, type: 'my-skill' })))
    this.$set(this, 'skillsPoolDirty', clone(this.skillsPool))
  }

  skillColor (skill: SkillType) {
    switch (skill.type) {
      case 'my-skill': return 'primary'
      case '1': return 'orange-10'
      case '2': return 'orange-8'
      case '3': return 'orange-6'
    }
    return 'orange'
  }

  get allowEdit () {
    return this.inEditing && !this.briefView
  }
}
</script>

<style lang="scss" scoped>
.skill-tag {
  margin-top: 0.2em;
  &:hover {
    opacity: 0.9;
  }
}

.allowEdit {
  .skill-area {
    padding: 1em;
    border-width: 0.5em;
  }
  .skill-tag {
    margin-bottom: 0.4em;
    animation: swaggering 250ms infinite;
    animation-timing-function: ease-in-out;
  }
}

.skill-area {
  border: 0 dashed;
  transition: all 700ms;
  &.skill-my {
    border-color: $indigo-2;
    &.drop-allowed {
      animation: flashing-area 2s infinite ease-in-out;
    }
  }
  &.skill-pool {
    border-color: $orange-2;
    //background: $orange-1;
 }
}

.draggable {
  display: inline-flex;
  flex-direction: column;
}

.skill-refresh-btn {
  transition: all 200ms;
  transform: scale(1);
  &:hover {
    transform: scale(1.15);
  }
}

.area-title {
  font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif;
  font-size: 1em;
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

@keyframes flashing-area {
  0% {
    border-color: $indigo-4;
    background: $indigo-1;
  }
  40% {
    border-color: $indigo-2;
    background: none;
  }
  60% {
     border-color: $indigo-2;
     background: none;
   }
  100% {
    border-color: $indigo-4;
    background: $indigo-1;
  }
}
</style>
