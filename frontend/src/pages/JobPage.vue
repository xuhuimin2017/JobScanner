<template>
  <q-page class="column items-center">
    <listing-view
      :job-data-list="rcmJobList"
      @select="onSelectJob">
    </listing-view>
    <JDView
      v-if="currentPreviewJdIdx !== null"
      :job-data="rcmJobList[currentPreviewJdIdx]">
    </JDView>
  </q-page>
</template>

<script lang="ts">
import ListingView from 'components/ListingView.vue'
import JDView from 'components/JDView.vue'
import { Vue, Component } from 'vue-property-decorator'

import sampleList from 'components/sample.json'
// console.log(sampleList)

@Component({
  components: { ListingView, JDView }
})
export default class UploadPage extends Vue {
  currentPreviewJdIdx: number | null = null

  get rcmJobList() {
    return sampleList
  }
  onSelectJob(idx) {
    // console.log(idx)
    this.currentPreviewJdIdx = idx
  }
}
</script>
