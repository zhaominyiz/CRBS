<template>
  <div class="line-numbers">
    <pre class="language-java line-numbers"><code class="language-java" v-html="code"></code></pre>
    <!--    <VueMarkdown :source="code"></VueMarkdown>-->
  </div>

</template>
<script>
  // import Vue from 'vue';
  import Prism from 'prismjs'
  import VueMarkdown from 'vue-markdown'

  export default {
    data() {
      return {
        code:
          '',
        urls:
          ''
      }
    },
    mounted() {
      var data = {
        userName: sessionStorage.getItem('username'),
        id: sessionStorage.getItem('taskid')
      }
      console.log(data)
      this.$http.post('api/getdetail', data).then(
        (Response) => {
          //this.code = Prism.highlight(Response.body.nowText, Prism.languages.java, 'java');
          this.urls = Response.body.nowFile;
          //this.code = Response.body.nowText.trimRight();
          let text = Response.body.nowText;

          // this.code = '```java\n' + text;
          // console.log("Receive\n"+text)
          text = text.replace(/</g, "&lt;")
          text = text.replace(/>/g, "&gt;")
          this.code = text.trimRight() + '\n ';
          this.$nextTick(() => {
            Prism.highlightAll();
          });
        }
      )
    },
    computed: {},
    methods: {},
    components: {
      VueMarkdown,
      'code-fragment': require('./codeFragment.vue')
    }
  }
</script>
<style scope>
  .code {
    max-height: 500px;
    overflow: scroll;
  }

  /**
* GHColors theme by Avi Aryan (http://aviaryan.in)
* Inspired by Github syntax coloring
*/
  pre[class*=language-].line-numbers {
    position: relative;
    padding-left: 3.8em;
    counter-reset: linenumber;
    white-space: pre-wrap;
  }

  pre[class*=language-].line-numbers > code {
    position: relative;
    white-space: inherit
  }

  .line-numbers .line-numbers-rows {
    position: absolute;
    pointer-events: none;
    top: 0;
    font-size: 100%;
    left: -3.8em;
    width: 3em;
    letter-spacing: -1px;
    border-right: 1px solid #999;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none
  }

  .line-numbers-rows > span {
    pointer-events: none;
    display: block;
    counter-increment: linenumber
  }

  .line-numbers-rows > span:before {
    content: counter(linenumber);
    color: #999;
    display: block;
    padding-right: .8em;
    text-align: right
  }

  code[class*="language-"],
  pre[class*="language-"] {
    color: #393A34;
    font-family: "Consolas", "Bitstream Vera Sans Mono", "Courier New", Courier, monospace;
    direction: ltr;
    text-align: left;
    white-space: pre;
    word-spacing: normal;
    word-break: normal;
    font-size: 0.95em;
    line-height: 1.2em;

    -moz-tab-size: 4;
    -o-tab-size: 4;
    tab-size: 4;

    -webkit-hyphens: none;
    -moz-hyphens: none;
    -ms-hyphens: none;
    hyphens: none;
  }

  pre[class*="language-"]::-moz-selection, pre[class*="language-"] ::-moz-selection,
  code[class*="language-"]::-moz-selection, code[class*="language-"] ::-moz-selection {
    background: #b3d4fc;
  }

  pre[class*="language-"]::selection, pre[class*="language-"] ::selection,
  code[class*="language-"]::selection, code[class*="language-"] ::selection {
    background: #b3d4fc;
  }

  /* Code blocks */
  pre[class*="language-"] {
    padding: 1em;
    margin: .5em 0;
    overflow: auto;
    border: 1px solid #dddddd;
    background-color: white;
  }

  /* :not(pre) > code[class*="language-"],
  pre[class*="language-"] {
  } */

  /* Inline code */
  :not(pre) > code[class*="language-"] {
    padding: .2em;
    padding-top: 1px;
    padding-bottom: 1px;
    background: #f8f8f8;
    border: 1px solid #dddddd;
  }

  .token.comment,
  .token.prolog,
  .token.doctype,
  .token.cdata {
    color: #999988;
    font-style: italic;
  }

  .token.namespace {
    opacity: .7;
  }

  .token.string,
  .token.attr-value {
    color: #e3116c;
  }

  .token.punctuation,
  .token.operator {
    color: #393A34; /* no highlight */
  }

  .token.entity,
  .token.url,
  .token.symbol,
  .token.number,
  .token.boolean,
  .token.variable,
  .token.constant,
  .token.property,
  .token.regex,
  .token.inserted {
    color: #36acaa;
  }

  .token.atrule,
  .token.keyword,
  .token.attr-name,
  .language-autohotkey .token.selector {
    color: #00a4db;
  }

  .token.function,
  .token.deleted,
  .language-autohotkey .token.tag {
    color: #9a050f;
  }

  .token.tag,
  .token.selector,
  .language-autohotkey .token.keyword {
    color: #00009f;
  }

  .token.important,
  .token.function,
  .token.bold {
    font-weight: bold;
  }

  .token.italic {
    font-style: italic;
  }

</style>
