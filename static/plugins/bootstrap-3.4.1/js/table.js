function selectExtra(allSelectName, sectionName) {
    let allSelect = document.querySelector(`#${allSelectName}`);
    let sectionOneInputs = document.querySelectorAll(`#${sectionName} input`);
    allSelect.addEventListener("click", () => {
        sectionOneInputs.forEach(value => {
            value.checked = allSelect.checked;
        });
    });
    sectionOneInputs.forEach(value => {
        value.addEventListener("click", () => {
            let flag = true;
            sectionOneInputs.forEach(valueContent => {
                if (!valueContent.checked) {
                    flag = false;
                }
                allSelect.checked = flag;
            });
        });
    });
};

window.addEventListener("load", () => {
    // 新增变压器
    let addTransformers = document.querySelector("#addTransformers");
    let masks = document.querySelector("#mask");
    let addPanel = document.querySelector("#addPanel");
    let cancel = document.querySelector("#cancel");
    addTransformers.addEventListener("click", () => {
        masks.style.display = "block";
        addPanel.style.display = "block";
    });
    cancel.addEventListener("click", () => {
        masks.style.display = "none";
        addPanel.style.display = "none";
        modifyPanel.style.display = "none";
    });
    // 修改变压器功能
    let tBody = document.querySelector("#maintable tbody");
    let deleteList = document.querySelectorAll(".delete");
    let modifyList = document.querySelectorAll(".modify");
    let modifyPanel = document.querySelector("#modifyPanel");
    let modifyCancel = document.querySelector("#modifycancel");
    let modifyInputs = [...document.querySelectorAll(".modify-inputs")];
    deleteList.forEach(deleteNode => {
        deleteNode.onclick = function() {
            tBody.removeChild(this.parentNode.parentNode);
        };
    });
    modifyList.forEach(modifyNode => {
        modifyNode.onclick = function() {
            let tdNodeList = [...this.parentNode.parentNode.children];
            console.log(modifyInputs.length)
            tdNodeList = tdNodeList.splice(1, 33);
            console.log(tdNodeList.length)
            tdNodeList.forEach((v, inum) => {
                modifyInputs[inum].value = v.innerText;
            });
            masks.style.display = "block";
            modifyPanel.style.display = "block";
        }
    });
    modifyCancel.addEventListener("click", () => {
        masks.style.display = "none";
        modifyPanel.style.display = "none";
    });
    // 导出Excel功能
    let exportbutton = document.querySelector(".bottom button");
    let cancelExcel = document.querySelector("#cancelExcel");
    let excelexp = document.querySelector("#excelexp");
    exportbutton.addEventListener("click", () => {
        masks.style.display = "block";
        excelexp.style.display = "block";
    });
    cancelExcel.addEventListener("click", () => {
        masks.style.display = "none";
        excelexp.style.display = "none";
    });
    // 全选功能
    selectExtra("basic-select1", "sectionOne");
    selectExtra("basic-select2", "sectionTwo");
    selectExtra("basic-select3", "sectionThree");
    // 表格区域滚动功能
    let mainTable = document.querySelector("#maintable");
    mainTable.addEventListener("wheel", (e) => {
        e.preventDefault();
        mainTable.scrollLeft += e.deltaY;
    });
    // 实现选择列冻结功能
    let lockButtons = document.querySelectorAll("#maintable span");
    let theadTds = document.querySelector("thead tr").children;
    let leftValue = 0;
    // 获取每行的tr
    let tbodyTrs = document.querySelectorAll("tbody tr");
    let lockList = [];
    for (let i = 0; i < lockButtons.length; i++) {
        lockButtons[i].addEventListener("click", () => {
            let lockTd = lockButtons[i].parentNode;
            for (let j = 0; j < theadTds.length; j++) {
                if (theadTds[j].innerText == lockTd.innerText) {
                    let index_ = lockList.indexOf(j);
                    if (index_ == -1) {
                        lockList.push(j);

                    } else {
                        lockList.splice(index_, 1);
                    }
                }
            }
            // 清除所有的样式
            for (let z = 1; z < 3; z++) {
                theadTds[z].style = " ";
                tbodyTrs.forEach((value) => {
                    value.children[z].style = " ";
                })
            }
            // 获取选中的列数据
            for (let x = 0; x < lockList.length; x++) {
                for (let y = 0; y < theadTds.length; y++) {
                    if (y == lockList[x]) {
                        leftValue = theadTds[y].clientWidth * x;
                        theadTds[y].style.position = "sticky";
                        theadTds[y].style.left = `${leftValue}px`;
                        theadTds[y].style.backgroundColor = "#399eea";
                        theadTds[y].style.color = "#fff";
                    }
                }
                tbodyTrs.forEach((value) => {
                    let tds = value.children[lockList[x]];
                    tds.style.position = "sticky";
                    tds.style.left = `${leftValue}px`;
                    tds.style.backgroundColor = "#399eea";
                    tds.style.color = "#fff";
                })
            }
        })
    }
})