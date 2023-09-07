var defaultPhysicsState = true;
var defaultGravitationalConstant = -2000;
var defaultCentralGravity = 0.3;
var defaultSpringLength = 95;
var defaultSpringConstant = 0.04;
var defaultAvoidOverlap = 0;


function resetAll() {
  var physics_switch = document.getElementById("switchPhysics");
  physics_switch.checked = defaultPhysicsState;

  var sliderGravitationalConstant = document.getElementById("sliderGravitationalConstant");
  sliderGravitationalConstant.value = defaultGravitationalConstant;

  var sliderCentralGravity = document.getElementById("sliderCentralGravity");
  sliderCentralGravity.value = defaultCentralGravity;

  var sliderSpringLength = document.getElementById("sliderSpringLength");
  sliderSpringLength.value = defaultSpringLength;

  var sliderSpringConstant = document.getElementById("sliderSpringConstant");
  sliderSpringConstant.value = defaultSpringConstant;

  var sliderAvoidOverlap = document.getElementById("sliderAvoidOverlap");
  sliderAvoidOverlap.value = defaultAvoidOverlap;
}

function resetPhysics() {
  resetAll();
  options.physics.enabled = defaultPhysicsState;
  network.setOptions(options);
}

document.addEventListener("DOMContentLoaded", function() {

  // Reset all options to default values
  resetAll();

  // Listen for changes in the gravitational constant slider
  var physics_switch = document.getElementById("switchPhysics");
  physics_switch.addEventListener("change", function() {
    if (physics_switch.checked) {
      options.physics.enabled = true;
      network.setOptions(options);
    } else {
      options.physics.enabled = false;
      network.setOptions(options);
    }
  });

});
