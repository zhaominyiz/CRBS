<script>
    var prePost = fs => {
        // console.log(fs)
        fs = fs || []
        var fs = fs.slice()
        for(let i=0; i<fs.length; i++){
            fs[i] = fs[i].slice()
            fs[i].push(i)   // fragment id
        }
        fs.sort( (a, b) => a[0] - b[0] )
        for(let i=1; i<fs.length; i++){
            fs[i][0] = Math.max(fs[i][0], fs[i-1][1])
            fs[i][1] = Math.max(fs[i][0], fs[i][1])     // 修正非法区间为空区间
        }
        // console.log('fs', fs)
        return fs   // l: int * r: int * id: int list
    }
    export default {
        name: 'CodeFragment',
        data () {
            return {
                colors: [
                    'red',
                    'blue',
                    'green',
                    '#3399ff',
                    'purple',
                ],
                prefix: Math.random().toString(36).substr(2)
            }
        },
        computed: {
            fs: function () {
                return prePost(this.fragments)
            }
        },
        methods: {
            scroll (id) {
                if(this.other){
                    // console.log('emit the id:', id)
                    this.other.$emit('scroll', id)
                }
            }
        },
        render (h) {
            var pos = 0
            var preList = []
            var fs = this.fs
            for(let [l, r, id] of this.fs){
                if(l != pos){
                    preList.push(
                        h('pre', {
                            style: {
                            }
                        }, [this.code.slice(pos, l)])
                    )
                }
                preList.push(
                    h('pre', {
                        style: {
                            color: this.colors[id % this.colors.length],
                        },
                        attrs: {
                            id: `${this.prefix}-${id}`,
                        },
                        on: {
                            // 注意, nativeOn不奏效. 
                            click: () => {
                                this.scroll(id)
                            }
                        },
                    },
                    [this.code.slice(l, r)])
                )
                pos = r
            }
            var last = fs[fs.length-1][1]
            preList.push(h('pre', {
                style: {
                }
            }, 
            [this.code.slice(last)]))
            return h('div', {
                style: {
                    height: '500px',
                    overflow: 'auto'
                }
            }, preList)
        },
        props: ['code', 'fragments'],
        created: function () {
        }
    }
</script>
<style scoped>
    pre {
        display: inline;
    }
</style>