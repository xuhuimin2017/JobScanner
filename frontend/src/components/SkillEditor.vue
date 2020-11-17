<template>
  <div class="column">
    <div class="row no-wrap skill-editor items-stretch justify-around" :class="{ allowEdit }">
      <div class="multiline-tag" :class="{ 'col-6 q-pr-md': allowEdit }">
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
                :color="skills.includes(item) ? 'primary' : 'orange'">{{ item }}</q-badge>
            </drag>
          </template>
          <template v-slot:feedback="{data}">
            <div class="draggable feedback" :key="data">
              <q-badge
                class="skill-tag q-mr-xs"
                text-color="white"
                outline
                :color="skills.includes(data) ? 'primary' : 'orange'">{{ data }}</q-badge>
            </div>
          </template>
        </drop-list>
      </div>

      <div class="multiline-tag col-6 q-pl-md" v-if="allowEdit">
        <drop-list
          :items="skillsPoolDirty"
          mode="cut"
          class="draggable-container full-height"
          @insert="onInsertSkill(skillsPoolDirty, $event)"
          @reorder="$event.apply(skillsPoolDirty)"
        >
          <template v-slot:item="{item}">
            <drag class="draggable" :key="item" :data="item" @cut="removeSkill(skillsPoolDirty, item)">
              <q-badge
                class="skill-tag q-mr-xs"
                text-color="white"
                :color="skills.includes(item) ? 'primary' : 'orange'">{{ item }}</q-badge>
            </drag>
          </template>
          <template v-slot:feedback="{data}">
            <div class="draggable feedback" :key="data">
              <q-badge
                class="skill-tag q-mr-xs"
                text-color="white"
                outline
                :color="skills.includes(data) ? 'primary' : 'orange'">{{ data }}</q-badge>
            </div>
          </template>
        </drop-list>
      </div>
    </div>

    <div class="row q-mt-md q-gutter-sm justify-center" v-if="allowEdit">
      <!--<q-btn rounded color="primary">Looks Good!</q-btn>-->
      <q-btn rounded flat color="primary" @click="onReset">Reset</q-btn>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop, Watch } from 'vue-property-decorator'
import { Drag, DropList } from 'vue-easy-dnd'
import { clone } from 'lodash'

@Component({
  components: {
    Drag, // eslint-disable-line @typescript-eslint/no-unsafe-assignment
    DropList // eslint-disable-line @typescript-eslint/no-unsafe-assignment
  }
})
export default class SkillEditor extends Vue {
  @Prop({ type: Array }) readonly skills?: [string];
  @Prop({ type: Array }) readonly skillsPool?: [{name: string, type: string}];
  @Prop({ type: Boolean, default: false }) readonly briefView?: boolean;
  @Prop({ type: Boolean, default: false }) readonly inEditing?: boolean;

  mounted () {
    this.onReset()
  }

  skillSelected = []
  skillsPoolDirty = []

  onInsertSkill<T> (list: Array<T>, event: {index, data}) {
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
    this.$set(this, 'skillSelected', clone(this.skills))
    this.$set(this, 'skillsPoolDirty', clone(this.skillsPool))
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
    //transform: scale(1.02);
    opacity: 0.9;
  }
}

.multiline-tag {
  //line-height: 1.3em !important;
}

.allowEdit {
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
