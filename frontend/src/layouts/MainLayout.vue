
<template>
  <q-layout view="hHh lpR fff" class="bg-white">
    <q-header bordered class="bg-white text-grey-8" height-hint="64">
      <q-toolbar class="GNL__toolbar q-pa-lg">

        <q-toolbar-title shrink class="row items-center no-wrap">
          <q-btn no-caps stretch flat :ripple="false" size="1em" @click="$router.push({name: 'upload'})">
            JobScanner
          </q-btn>
        </q-toolbar-title>

        <q-space />

        <div class="q-gutter-sm row items-center no-wrap">
          <q-btn v-if="$q.screen.gt.sm" round dense flat color="text-grey-7" icon="apps">
          </q-btn>
<!--          <q-btn round dense flat color="grey-8" icon="notifications">-->
<!--            <q-badge color="red" text-color="white" floating>-->
<!--              2-->
<!--            </q-badge>-->
<!--            <q-tooltip>Notifications</q-tooltip>-->
<!--          </q-btn>-->
<!--          <q-btn round flat>-->
<!--            <q-avatar size="26px">-->
<!--              <img src="https://cdn.quasar.dev/img/boy-avatar.png">-->
<!--            </q-avatar>-->
<!--            <q-tooltip>Account</q-tooltip>-->
<!--          </q-btn>-->
        </div>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
    <q-footer class="bg-white text-primary non-selectable text-center q-pa-md">
      <span class="footer-credit" @mouseenter="heartSuffix=''" @mouseleave="heartSuffix='-outline'">
        <q-icon :name="'mdi-heart'+heartSuffix"></q-icon>
        Created by <a href="#">Guangxue Wen</a>, <a href="#">Huimin Xu</a>, <a href="#">Lingfei Wu</a>
      </span>
    </q-footer>
  </q-layout>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'

@Component
export default class MainLayout extends Vue {
  conversations = []
  leftDrawerOpen = false
  heartSuffix = '-outline'
  get style () {
    return {
      height: `${this.$q.screen.height} px`
    }
  }
}
</script>

<style lang="scss" scoped>
.footer-credit {
  a, a:link, a:visited {
    color: $primary;
    text-decoration-color: lighten($primary, 30%);
    text-decoration-style: dotted;
    transition: all 500ms;
  }
  a:hover {
    text-decoration-color: lighten($primary, 0%);
    //text-decoration-style: dashed;
  }
}
</style>

<style lang="sass">
.GNL
  &__toolbar
    height: 64px
  &__drawer-item
    line-height: 24px
    border-radius: 0 24px 24px 0
    margin-right: 12px
    .q-item__section--avatar
      .q-icon
        color: #5f6368
    .q-item__label
      color: #3c4043
      letter-spacing: .01785714em
      font-size: .875rem
      font-weight: 500
      line-height: 1.25rem
  &__drawer-footer-link
    color: inherit
    text-decoration: none
    font-weight: 500
    font-size: .75rem
    &:hover
      color: #000
</style>
