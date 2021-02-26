qNumber = 1
$('#submit-survey').on('click', '#add-question-input', function(evt){
    evt.preventDefault();
    if( $('#question-inputs').children().length < 5){

        $('#question-inputs').append(`<input type="text" name="question${qNumber}" placeholder="Write Question" class="form-control my-2">`)
        console.log(qNumber)
        qNumber++;
    }else{
            $('#question-inputs').append('<div class="alert alert-danger id="max-questions" role="alert">Sorry, 5 questions max</div>')
        }
})