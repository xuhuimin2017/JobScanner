<template>
  <q-page class="column items-center">
    <div class="row no-wrap">
      <listing-view
        v-if="!isDetailShown"
        ref="listingView"
        :job-data-list="rcmJobList"
        :small="isDetailShown"
        @select="onSelectJob"
      >
      </listing-view>
      <JDView
        v-else
        :job-data="rcmJobList[currentPreviewJdIdx]"
        @close="isDetailShown = false"
      ></JDView>
    </div>
  </q-page>
</template>

<script lang="ts">
import ListingView from 'components/ListingView.vue'
import JDView from 'components/JDView.vue'
import {Vue, Component, Watch, Prop} from 'vue-property-decorator'

import sampleList from 'components/sample.json'
import {morph} from "quasar";
import {JobData} from "components/models";
// console.log(sampleList)

@Component({
  components: { ListingView, JDView }
})
export default class UploadPage extends Vue {
  @Prop({ type: Array, required: true }) readonly jobDataList!: JobData;

  currentPreviewJdIdx: number | null = null

  @Watch('currentPreviewJdIdx')
  onCurrentIdxChange(val: string, oldVal: string) {
    console.log('onchange')
    const onToggle = () => {
      console.log('on toggle')
    }

    // morph({
    //   from: this.$refs.listingView,
    //   onToggle,
    //   duration: 500,
    //   tween: true
    // })
  }

  get rcmJobList() {
    // return sampleList
    return this.jobDataList
  }

  get isDetailShown() {
    return this.currentPreviewJdIdx !== null
  }

  set isDetailShown(val) {
    if (!val) {
      this.currentPreviewJdIdx = null
    }
  }

  onSelectJob(idx) {
    // console.log(idx)
    this.currentPreviewJdIdx = idx
  }
}
</script>
