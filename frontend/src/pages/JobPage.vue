<template>
  <div>
    <listing-view
      v-if="!isDetailShown"
      ref="listingView"
      :job-data-list="rcmJobList"
      :my-skills="mySkills"
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
</template>

<script lang="ts">
import ListingView from 'components/ListingView.vue'
import JDView from 'components/JDView.vue'
import { Vue, Component, Prop } from 'vue-property-decorator'

import sampleBackendData from 'components/sample.json'
import { RecommendationModel } from 'components/models'
import { getIsDev } from 'src/utils/mode'

@Component({
  components: { ListingView, JDView }
})
export default class UploadPage extends Vue {
  @Prop({ type: Object }) readonly recommendationData!: RecommendationModel;

  currentPreviewJdIdx: number | null = null

  get dataProxy () {
    if (!this.recommendationData && getIsDev()) {
      console.warn('Using debug data')
      return sampleBackendData
    } else {
      // TODO show no data
    }
    return this.recommendationData
  }

  get rcmJobList () {
    return this.dataProxy.jobs
  }

  get mySkills () {
    return this.dataProxy.mySkills
  }

  get isDetailShown () {
    return this.currentPreviewJdIdx !== null
  }

  set isDetailShown (val) {
    if (!val) {
      this.currentPreviewJdIdx = null
    }
  }

  onSelectJob (idx: number) {
    // console.log(idx)
    this.currentPreviewJdIdx = idx
  }
}
</script>
