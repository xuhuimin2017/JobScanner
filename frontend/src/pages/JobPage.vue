<template>
  <q-page class="column items-center">
    <listing-view :job-data-list="rcmJobList"></listing-view>
    <JDView :job-data="rcmJobList[1]"></JDView>
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
  get rcmJobList() {
    return sampleList
  }
}
</script>
