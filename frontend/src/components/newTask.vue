<template>
  <div>
    <Card style="width:100%; height:100%">
      <Row slot="title">
        <Steps :current="step">
          <Step title="基本信息" content="填写标题, 任务描述"></Step>
          <Step title="参数设定" content="选取算法, 语言等参数"></Step>
          <Step title="文件上传" content="上传代码"></Step>
        </Steps>
      </Row>
      <!--<a href="#" slot="extra" @click.prevent="changeLimit">
          <Icon type="ios-loop-strong"></Icon>
          换一换
      </a>-->
      <Row>
        <Form v-if="step==0" :model="uploadForm" :label-width="80">
          <Form-item label="标题">
            <Input v-model="uploadForm.caption" placeholder="caption"></Input>
          </Form-item>
          <Form-item label="描述">
            <Input type="textarea" :rows="5" v-model="uploadForm.description" placeholder="description"></Input>
          </Form-item>
          <Row type="flex" justify="center">
            <Col>
              <Button @click="nextStep" type="primary" shape="circle" icon="chevron-right"></Button>
            </Col>
          </Row>
        </Form>
        <Form v-if="step==1" :model="uploadForm" :label-width="80">
          <Form-item label="算法">
            <Select v-model="uploadForm.algorithm" style="width:200px">
              <Option v-for="algo in algorithms" :value="algo.value" :key="algo">{{ algo.label }}</Option>
            </Select>
          </Form-item>
          <Form-item label="语言">
            <Select v-model="uploadForm.lang" style="width:200px">
              <Option v-for="lang in langs" :value="lang.value" :key="lang">{{ lang.label }}</Option>
            </Select>
          </Form-item>
          <Form-item label="循环语句">
            <Select v-model="uploadForm.lop" style="width:200px">
              <Option v-for="lop in lops" :value="lop.value" :key="lop">{{ lop.label }}</Option>
            </Select>
          </Form-item>
          <Form-item label="switch语句">
            <Select v-model="uploadForm.select" style="width:200px">
              <Option v-for="select in selects" :value="select.value" :key="select">{{ select.label }}</Option>
            </Select>
          </Form-item>
          <Form-item label="if语句">
            <Select v-model="uploadForm.multiif" style="width:200px">
              <Option v-for="multiif in multiifs" :value="multiif.value" :key="multiif">{{ multiif.label }}</Option>
            </Select>
          </Form-item>
          <!--                    <Form-item label="长度阈值">-->
          <!--                        <Slider :min="4" :max="50" v-model="uploadForm.tlen" :tip-format="tlenFormat" show-input></Slider>-->
          <!--                    </Form-item>-->
          <!--                    <Form-item label="相似度阈值">-->
          <!--                        <Slider v-model="uploadForm.similarity" :tip-format="simFormat" show-input></Slider>-->
          <!--                    </Form-item>-->
          <Row type="flex" :gutter="32" justify="center">
            <Col>
              <Button @click="prevStep" type="primary" shape="circle" icon="chevron-left"></Button>
            </Col>
            <Col>
              <Button @click="nextStep" type="primary" shape="circle" icon="chevron-right"></Button>
            </Col>
          </Row>
        </Form>
        <Form v-if="step==2" :model="uploadForm" :label-width="80">
          <!--                     <Upload-->
          <!--                        multiple-->
          <!--                        type="drag"-->
          <!--                        action="http://localhost:8666/api/coderebuild"-->
          <!--                        :headers="uploadHeaders"-->
          <!--                        :data="uploadData"-->
          <!--                        >-->
          <!--                        <div style="padding: 20px 0">-->
          <!--                            <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>-->
          <!--                            <p>点击或将文件拖拽到这里上传</p>-->
          <!--                        </div>-->
          <!--                    </Upload>-->
          <Upload
            ref="upload"
            action="http://localhost:8666/api/coderebuild"
            :data="uploadData"
            :on-success="UploadSuccess"
            :before-upload="handleBeforeUpload"
            :on-eroor="UploadFailed"
          >
            <i-button type="info" class="btn btn-file" icon="ios-cloud-upload-outline"
                      style="width:100%;">选择附件
            </i-button>
          </Upload>

          <Row type="flex" :gutter="32" justify="center">
            <Col>
              <Button @click="prevStep" type="primary" shape="circle" icon="chevron-left"></Button>
            </Col>
          </Row>
        </Form>
      </Row>
    </Card>


  </div>
</template>


<script>
  export default {
    data() {
      return {
        step: 0,
        uploadForm: {
          caption: "",
          description: "",
          lang: "",
          // prep_list: ["comment", "spec-keyword", "spec-punctuation"],
          algorithm: "",
          lop: "",
          select: "",
          multiif: "",
          userName: ""
        },
        uploadData: {},
        langs: [
          {
            'value': 'JAVA',
            'label': 'JAVA语言'
          }
        ],
        algorithms: [
          {
            'value': 'Standard',
            'label': '采用语法树分析的标准算法'
          }
        ],
        lops: [
          {
            'value': '0',
            'label': '不予以操作'
          },
          {
            'value': '1',
            'label': '将for语句转成while语句'
          }, {
            'value': '2',
            'label': '将while语句转成for语句'
          }
        ],
        selects: [
          {
            'value': '0',
            'label': '不予以操作'
          },
          {
            'value': '1',
            'label': '将switch语句转if语句'
          }, {
            'value': '2',
            'label': '将if语句转成switch语句'
          }
        ],
        multiifs: [
          {
            'value': '0',
            'label': '不予以操作'
          },
          {
            'value': '1',
            'label': '将一条if语句转多条if语句'
          }, {
            'value': '2',
            'label': '将多条if语句转一条if语句'
          }
        ]
      }
    },
    methods: {
      prevStep() {
        this.step -= 1;
      },
      nextStep() {
        this.step += 1
      },
      UploadSuccess() {
        this.$Message.success("成功提交队列，请于记录中检查结果")
      },
      UploadFailed() {
        this.$Message.error("网络异常！")
      },
      handleBeforeUpload(ufile) {
        var form = this.uploadForm
        this.uploadData = {
          algorithm: form.algorithm,
          caption: form.caption,
          description: form.description,
          lang: form.lang,
          lop: form.lop,
          select: form.select,
          multiif: form.multiif,
          userName: sessionStorage.getItem('username'),
          file: ufile
        }
        console.log(this.uploadData)
        let promise = new Promise((resolve) => {
          this.$nextTick(function () {
            resolve(true);
          });
        });
        // alert("DO THIS"+ufile)
        return promise; //通过返回一个promis对象解决
      }
    },
    computed: {
      addheaders() {
        return {
          "Access-Control-Allow-Origin:": "*"
        }
      }
    }
  }
</script>
