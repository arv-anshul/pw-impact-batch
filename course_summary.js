// TODO: You have to replace the class names to work this for you.

// ----------------------- Toggle every sections ------------------------ //
const elements = document.querySelectorAll(
  ".LessonList_lesson-list__160f2 > div:nth-child(n)"
);

console.log("Toggled:", elements.length + 1, "Sections");

for (let i = 1; i < elements.length + 1; i++) {
  selector = `.LessonList_lesson-list__160f2 > div:nth-child(${i}) > div:nth-child(1)`;

  document.querySelector(selector).click();
}

// --------------------- GET Submitted / Un-submitted -------------------------- //
const quizAssignment = {
  "Marked List":
    ".LessonList_lesson-list__160f2 .LessonList_section-list__30ZP5 .LessonList_status__268gc.LessonList_marked__1gnfe",
  "Total Assignment": ".fa-file-alt",
  "Submitted Quiz": ".fa-redo",
  "Un-Submitted Quiz": ".fa-question-circle",
};

const video = {
  "Checked Video":
    ".LessonList_lesson-list__160f2 .LessonList_section-list__30ZP5 .LessonList_section-list-video__2Xcf5 input[checked]",
  "Un-Checked Video":
    ".LessonList_lesson-list__160f2 .LessonList_section-list__30ZP5 .LessonList_section-list-video__2Xcf5 input:not([checked])",
};

for (const key in video) {
  ele = document.querySelectorAll(video[key]);
  console.log(`${key}: ${ele.length}`);
}

nAssSubmitted = 0;
for (const key in quizAssignment) {
  ele = document.querySelectorAll(quizAssignment[key]);

  if (key == "Marked") {
    for (let i = 1; i < ele.length; i++) {
      if (ele[i].innerHTML == "Marked") {
        nAssSubmitted += 1;
      }
    }
    console.log(`Submitted Assignment: ${nAssSubmitted}`);
  } else if (key == "Total Assignment") {
    console.log(`Un-Submitted Assignment: ${ele.length - nAssSubmitted}`);
  } else {
    console.log(`${key}: ${ele.length}`);
  }
}

// ------------ Get section name of Un-Checked Videos ------------------ //
let unCheckedVideos = document.querySelectorAll(video["Un-Checked Video"]);
for (const ele of unCheckedVideos) {
  // txt = ele.parentNode.childNodes[1].innerText.split("\n")[0];
  txt =
    ele.parentNode.parentNode.parentNode.parentNode.parentNode.firstElementChild
      .firstElementChild.firstElementChild.innerText;
  console.log(txt);
}
