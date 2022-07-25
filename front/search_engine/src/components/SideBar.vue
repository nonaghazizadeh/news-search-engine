<template>
  <div>
      <VueSidebarMenuAkahon 
      :menu-items=menuItems 
      :menu-title=menuTitle 
      :menu-icon=menuIcon
      :profile-img=profileImg 
      :profile-name=profileName
      :profile-role=profileRole
      :is-exit-button=isExitButton
      :secondary-color=secondaryColor
      :is-search=isSearch
       />
  </div>
</template>

<script>
  import VueSidebarMenuAkahon from "vue-sidebar-menu-akahon";
  
  export default {
    name: 'component.vue',
    components: {VueSidebarMenuAkahon},
    data() {
      return {
        secondaryColor: '#11101d',
        profileImg : '',
        profileName: '',
        profileRole: '',
        isExitButton: false,
        isSearch: false,
        menuTitle : 'Search Engine',
        menuIcon: 'bx-search-alt-2',
        menuItems: [
        {link: '/boolean',name: 'Boolean search', tooltip: 'Boolean search', icon: 'bx-grid-alt' }, 
        {link: '/tfidf',name: 'TF-IDF search', tooltip: 'TF-IDF search', icon: 'bx-grid-alt' },
        {link: '/fasttext',name: 'Fasttext search', tooltip: 'Fasttext search', icon: 'bx-grid-alt' },
        {link: '/transformer',name: 'Transformer search', tooltip: 'Transformer search', icon: 'bx-grid-alt' },
        {link: '/elastic',name: 'Elastic search', tooltip: 'Elastic search', icon: 'bx-grid-alt' },
        {link: '/classification-transformers',name: 'Classification transformers', tooltip: 'Classification transformers', icon: 'bx-grid-alt' },
        {link: '/classification-logistic-regression',name: 'Classification Logistic Regression', tooltip: 'Classification Logistic Regression', icon: 'bx-grid-alt' },
        {link: '/clustering',name: 'Clustering', tooltip: 'Clustering', icon: 'bx-grid-alt' },
        {link: '/pagerank',name: 'PageRank link analysis', tooltip: 'PageRank link analysis', icon: 'bx-grid-alt' },
        {link: '/hits',name: 'HITS link analysis', tooltip: 'HITS link analysis', icon: 'bx-grid-alt' }
        ]
      }
    }
  }
</script>

<style>
.sidebar div .profile-details {
    display: none !important
}
.sidebar.open{
    width: 360px !important
}
</style>
