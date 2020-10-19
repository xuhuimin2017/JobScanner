<template>
  <q-page class="column items-center">
    <div class="row no-wrap">
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
  </q-page>
</template>

<script lang="ts">
import ListingView from 'components/ListingView.vue'
import JDView from 'components/JDView.vue'
import { Vue, Component, Prop } from 'vue-property-decorator'

// import sampleList from 'components/sample.json'
import { RecommendationModel } from 'components/models'

@Component({
  components: { ListingView, JDView }
})
export default class UploadPage extends Vue {
  @Prop({ type: Object, required: true }) readonly recommendationData!: RecommendationModel;

  currentPreviewJdIdx: number | null = null

  // @Watch('currentPreviewJdIdx')
  // onCurrentIdxChange (val: string, oldVal: string) {
  //   console.log('onchange')
  //
  //   // morph({
  //   //   from: this.$refs.listingView,
  //   //   onToggle,
  //   //   duration: 500,
  //   //   tween: true
  //   // })
  // }

  get rcmJobList () {
    // return sampleList
    return this.recommendationData.jobs
  }

  get mySkills () {
    return this.recommendationData.mySkills
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
