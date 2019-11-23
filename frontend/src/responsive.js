// Equivalent of jQuery .ready
document.addEventListener('DOMContentLoaded', function () {

  // Initialize variables
  var lastScrollTop = window.pageYOffset || document.documentElement.scrollTop; // Scroll position of body

  // Listener to resizes
  window.onresize = function (event) {
    lastScrollTop = window.pageYOffset || document.documentElement.scrollTop;
  };

  // Helper functions
  // Detect offset of element
  function getOffset(el) {
    var _x = 0;
    var _y = 0;
    while (el && !isNaN(el.offsetLeft) && !isNaN(el.offsetTop)) {
      _x += el.offsetLeft - el.scrollLeft;
      _y += el.offsetTop - el.scrollTop;
      el = el.offsetParent;
    }
    return {top: _y, left: _x};
  };

  // Add class to element => https://www.sitepoint.com/add-remove-css-class-vanilla-js/
  function addNewClass(elements, myClass) {
    // if there are no elements, we're done
    if (!elements) {
      return;
    }
    // if we have a selector, get the chosen elements
    if (typeof (elements) === 'string') {
      elements = document.querySelectorAll(elements);
    }
    // if we have a single DOM element, make it an array to simplify behavior
    else if (elements.tagName) {
      elements = [elements];
    }
    // add class to all chosen elements
    for (var i = 0; i < elements.length; i++) {
      // if class is not already found
      if ((' ' + elements[i].className + ' ').indexOf(' ' + myClass + ' ') < 0) {
        // add class
        elements[i].className += ' ' + myClass;
      }
    }
  };

  // Remove class from element => https://www.sitepoint.com/add-remove-css-class-vanilla-js/
  function removeClass(elements, myClass) {
    // if there are no elements, we're done
    if (!elements) {
      return;
    }

    // if we have a selector, get the chosen elements
    if (typeof (elements) === 'string') {
      elements = document.querySelectorAll(elements);
    }
    // if we have a single DOM element, make it an array to simplify behavior
    else if (elements.tagName) {
      elements = [elements];
    }
    // create pattern to find class name
    var reg = new RegExp('(^| )' + myClass + '($| )', 'g');
    // remove class from all chosen elements
    for (var i = 0; i < elements.length; i++) {
      elements[i].className = elements[i].className.replace(reg, ' ');
    }
  }

  // Smooth scrolling => https://codepen.io/andylobban/pen/qOLKVW
  if ('querySelector' in document && 'addEventListener' in window && Array.prototype.forEach) {
    // Function to animate the scroll
    var smoothScroll = function (anchor, duration) {
      // Calculate how far and how fast to scroll
      var startLocation = window.pageYOffset;
      var endLocation = anchor.offsetTop - 40; // Remove 40 pixels for padding
      var distance = endLocation - startLocation;
      var increments = distance / (duration / 16);
      var stopAnimation;
      // Scroll the page by an increment, and check if it's time to stop
      var animateScroll = function () {
        window.scrollBy(0, increments);
        stopAnimation();
      };
      // If scrolling down
      if (increments >= 0) {
        // Stop animation when you reach the anchor OR the bottom of the page
        stopAnimation = function () {
          var travelled = window.pageYOffset;
          if ((travelled >= (endLocation - increments)) || ((window.innerHeight + travelled) >= document.body.offsetHeight)) {
            clearInterval(runAnimation);
          }
        };
      }
      // Loop the animation function
      var runAnimation = setInterval(animateScroll, 16);
    };
    // Define smooth scroll links
    var scrollToggle = document.querySelectorAll('.scroll');
    // For each smooth scroll link
    [].forEach.call(scrollToggle, function (toggle) {
      // When the smooth scroll link is clicked
      toggle.addEventListener('click', function (e) {
        // Prevent the default link behavior
        e.preventDefault();
        // Get anchor link and calculate distance from the top
        var dataTarget = document.querySelector('.landing__section');
        var dataSpeed = toggle.getAttribute('data-speed');
        // If the anchor exists
        if (dataTarget) {
          // Scroll to the anchor
          smoothScroll(dataTarget, dataSpeed || 700);
        }
      }, false);
    });
  }


  // Listen to scroll position changes
  window.addEventListener("scroll", function () {

    // NAVIGATION BAR ON LANDING FIXED
    // If there is a #navConverter element then attach listener to scroll events
    if (document.body.contains(document.getElementById("navConverter"))) {
      var lastScrollTop = window.pageYOffset || document.documentElement.scrollTop;
      // if the current body position is less than 20 pixels away from our converter, convert
      if (lastScrollTop > (getOffset(document.getElementById('navConverter')).top - 60)) {
        removeClass(document.querySelector('.navbar'), 'navbar--extended');
      } else {
        addNewClass(document.querySelector('.navbar'), 'navbar--extended');
      }
    }

    // SCROLL TO NEXT ELEMENT ON LANDING
    if (document.body.contains(document.getElementById('scrollToNext'))) {
      var lastScrollTop = window.pageYOffset || document.documentElement.scrollTop;
      // if the current body position is less than 20 pixels away from the top, hide the icon
      if (lastScrollTop > 20) {
        addNewClass(document.getElementById('scrollToNext'), 'invisible');
      } else {
        removeClass(document.getElementById('scrollToNext'), 'invisible');
      }
    }
  });

  // Responsive mobile menu
  // Create the menu
  if (document.getElementsByClassName("nav__mobile") && document.getElementsByClassName('nav__mobile').length > 0) {
    var navElements = document.getElementsByClassName('navbar__menu')[0].innerHTML;
    document.getElementsByClassName('nav__mobile')[0].innerHTML = navElements;
    // Load
    var nav = responsiveNav(".nav__mobile", { // Selector
      animate: true, // Boolean: Use CSS3 transitions, true or false
      transition: 284, // Integer: Speed of the transition, in milliseconds
      label: "Menu", // String: Label for the navigation toggle
      insert: "before", // String: Insert the toggle before or after the navigation
      customToggle: "toggle", // Selector: Specify the ID of a custom toggle
      openPos: "relative", // String: Position of the opened nav, relative or static
      navClass: "nav__mobile", // String: Default CSS class. If changed, you need to edit the CSS too!
    });
  } else {
    addNewClass(document.querySelector('.navbar__menu'), 'navbar__menu--noMob');
    addNewClass(document.querySelector('.navbar__menu-mob'), 'navbar__menu-mob--noMob');
  }
  ;
});
(function (f) {
  if (typeof exports === "object" && typeof module !== "undefined") {
    module.exports = f()
  } else if (typeof define === "function" && define.amd) {
    define([], f)
  } else {
    var g;
    if (typeof window !== "undefined") {
      g = window
    } else if (typeof global !== "undefined") {
      g = global
    } else if (typeof self !== "undefined") {
      g = self
    } else {
      g = this
    }
    g.flexibility = f()
  }
})(function () {
  var define, module, exports;
  return (function e(t, n, r) {
    function s(o, u) {
      if (!n[o]) {
        if (!t[o]) {
          var a = typeof require == "function" && require;
          if (!u && a) return a(o, !0);
          if (i) return i(o, !0);
          var f = new Error("Cannot find module '" + o + "'");
          throw f.code = "MODULE_NOT_FOUND", f
        }
        var l = n[o] = {exports: {}};
        t[o][0].call(l.exports, function (e) {
          var n = t[o][1][e];
          return s(n ? n : e)
        }, l, l.exports, e, t, n, r)
      }
      return n[o].exports
    }

    var i = typeof require == "function" && require;
    for (var o = 0; o < r.length; o++) s(r[o]);
    return s
  })({
    1: [function (require, module, exports) {
      module.exports = function alignContent(target) {
        var start;
        var factor;

        if (target.lines.length < 2 || target.alignContent === 'stretch') {
          factor = target.crossSpace / target.lines.length;
          start = 0;

          target.lines.forEach(function (line) {
            line.crossStart = start;
            line.cross += factor;

            start += line.cross;
          });
        } else if (target.alignContent === 'flex-start') {
          start = 0;

          target.lines.forEach(function (line) {
            line.crossStart = start;

            start += line.cross;
          });
        } else if (target.alignContent === 'flex-end') {
          start = target.crossSpace;

          target.lines.forEach(function (line) {
            line.crossStart = start;

            start += line.cross;
          });
        } else if (target.alignContent === 'center') {
          start = target.crossSpace / 2;

          target.lines.forEach(function (line) {
            line.crossStart = start;

            start += line.cross;
          });
        } else if (target.alignContent === 'space-between') {
          factor = target.crossSpace / (target.lines.length - 1);
          start = 0;

          target.lines.forEach(function (line) {
            line.crossStart = start;

            start += line.cross + factor;
          });
        } else if (target.alignContent === 'space-around') {
          factor = target.crossSpace * 2 / (target.lines.length * 2);
          start = factor / 2;

          target.lines.forEach(function (line) {
            line.crossStart = start;

            start += line.cross + factor;
          });
        } else if (target.alignContent === 'stretch') {
          factor = target.crossSpace / target.lines.length;
          start = 0;

          target.lines.forEach(function (line) {
            line.crossStart = start;
            line.cross += factor;

            start += line.cross;
          });
        }
      };

    }, {}],
    2: [function (require, module, exports) {
      module.exports = function alignItems(target) {
        target.lines.forEach(function (line) {
          line.children.forEach(function (child) {
            if (child.alignSelf === 'flex-start') {
              child.crossStart = line.crossStart;
            } else if (child.alignSelf === 'flex-end') {
              child.crossStart = line.crossStart + line.cross - child.crossAround;
            } else if (child.alignSelf === 'center') {
              child.crossStart = line.crossStart + (line.cross - child.crossAround) / 2;
            } else if (child.alignSelf === 'stretch') {
              child.crossStart = line.crossStart;
              child.crossAround = line.cross;
            }
          });
        });
      };

    }, {}],
    3: [function (require, module, exports) {
      module.exports = function flexDirection(target, targetFlexDirection, targetAlignItems) {
        var clientRect = target.node.getBoundingClientRect();

        if (targetFlexDirection === 'row' || targetFlexDirection === 'row-reverse') {
          target.mainAxis = 'inline';
          target.crossAxis = 'block';

          if (typeof target.main === 'number' || typeof target.cross === 'number') {
            if (target.flexDirection === 'row' || targetFlexDirection === 'row-reverse') {
              target.width = target.main;
              target.height = target.cross;
            } else {
              target.width = target.cross;
              target.height = target.main;
            }
          }

          target.main = target.width;
          target.cross = target.height;

          target.mainClient = clientRect.width || target.node.offsetWidth;
          target.crossClient = clientRect.height || target.node.offsetHeight;

          target.mainBefore = target.marginLeft;
          target.mainAfter = target.marginRight;
          target.crossBefore = target.marginTop;
          target.crossAfter = target.marginBottom;
        } else {
          target.mainAxis = 'block';
          target.crossAxis = 'inline';

          target.main = target.height;
          target.cross = target.width;

          if (typeof target.main === 'number' || typeof target.cross === 'number') {
            if (target.flexDirection === 'column' || targetFlexDirection === 'column-reverse') {
              target.width = target.cross;
              target.height = target.main;
            } else {
              target.width = target.main;
              target.height = target.cross;
            }
          }

          target.mainClient = clientRect.height || target.node.offsetHeight;
          target.crossClient = clientRect.width || target.node.offsetWidth;

          target.mainBefore = target.marginTop;
          target.mainAfter = target.marginBottom;
          target.crossBefore = target.marginLeft;
          target.crossAfter = target.marginRight;
        }

        if (typeof target.flexBasis === 'number') {
          target.main = target.flexBasis;
        }

        if (target.main === 'auto') {
          target.mainAround = target.mainClient;
        } else {
          target.mainAround = target.main;
        }

        if (target.cross === 'auto') {
          target.crossAround = target.crossClient;
        } else {
          target.crossAround = target.cross;
        }

        if (typeof target.mainBefore === 'number') {
          target.mainAround += target.mainBefore;
        }

        if (typeof target.mainAfter === 'number') {
          target.mainAround += target.mainAfter;
        }

        if (typeof target.crossBefore === 'number') {
          target.crossAround += target.crossBefore;
        }

        if (typeof target.crossBefore === 'number') {
          target.crossAround += target.crossBefore;
        }

        if (target.alignSelf === 'auto') {
          target.alignSelf = targetAlignItems;
        }
      };

    }, {}],
    4: [function (require, module, exports) {
      module.exports = function flexGrow(line) {
        if (line.mainSpace > 0) {
          var growFactor = line.children.reduce(function (lastGrowFactor, child) {
            return lastGrowFactor + child.flexGrow;
          }, 0);

          if (growFactor > 0) {
            line.children.forEach(function (child) {
              child.mainAround += child.flexGrow / growFactor * line.mainSpace;
            });

            line.main = line.children.reduce(function (main, child) {
              return main + child.mainAround;
            }, 0);

            line.mainSpace = 0;
          }
        }
      };

    }, {}],
    5: [function (require, module, exports) {
      module.exports = function flexShrink(line) {
        if (line.mainSpace < 0) {
          var shrinkFactor = line.children.reduce(function (lastShrinkFactor, child) {
            return lastShrinkFactor + child.flexShrink;
          }, 0);

          if (shrinkFactor > 0) {
            line.children.forEach(function (child) {
              child.mainAround += child.flexShrink / shrinkFactor * line.mainSpace;
            });

            line.main = line.children.reduce(function (main, child) {
              return main + child.mainAround;
            }, 0);

            line.mainSpace = 0;
          }
        }
      };

    }, {}],
    6: [function (require, module, exports) {
      module.exports = function flexboxLines(target) {
        var line;

        target.lines = [line = {
          main: 0,
          cross: 0,
          children: []
        }];

        target.children.forEach(function (child) {
          if (
            target.flexWrap === 'nowrap' ||
            line.children.length === 0 ||
            target.mainAround >= line.main + child.mainAround
          ) {
            line.main += child.mainAround;
            line.cross = Math.max(line.cross, child.crossAround);
          } else {
            target.lines.push(line = {
              main: child.mainAround,
              cross: child.crossAround,
              children: []
            });
          }

          line.children.push(child);
        });
      };

    }, {}],
    7: [function (require, module, exports) {
      module.exports = function flexbox(target) {
        target.descendants.forEach(function (descendant) {
          module.exports(descendant);
        });

        if (target.display === 'flex') {
          target.children.forEach(function (child) {
            require('./flex-direction')(child, target.flexDirection, target.alignItems);
          });
        } else {
          return target;
        }

        require('./order')(target);
        require('./flex-direction')(target, target.flexDirection, target.alignItems);
        require('./flexbox-lines')(target);

        if (target.main === 'auto') {
          target.main = Math.max(target.mainAround, target.lines.reduce(function (main, line) {
            return Math.max(main, line.main);
          }, 0));

          if (target.flexDirection === 'row') {
            target.mainAround = target.mainClient + target.mainBefore + target.mainAfter;
          } else {
            target.mainAround = target.main + target.mainBefore + target.mainAfter;
          }
        }

        if (target.cross === 'auto') {
          target.cross = target.lines.reduce(function (cross, line) {
            return cross + line.cross;
          }, 0);

          if (target.flexDirection === 'column') {
            target.crossAround = target.crossClient + target.crossBefore + target.crossAfter;
          } else {
            target.crossAround = target.cross + target.crossBefore + target.crossAfter;
          }

          target.crossSpace = target.crossAround - target.cross;
        } else {
          target.crossSpace = target.cross - target.lines.reduce(function (cross, line) {
            return cross + line.cross;
          }, 0);
        }

        require('./align-content')(target);

        target.lines.forEach(function (line) {
          line.mainSpace = target.main - line.main;

          require('./flex-grow')(line);
          require('./flex-shrink')(line);
          require('./margin-main')(line);
          require('./margin-cross')(line);
          require('./justify-content')(line, target.justifyContent);
        });

        require('./align-items')(target);

        return target;
      };

    }, {
      "./align-content": 1,
      "./align-items": 2,
      "./flex-direction": 3,
      "./flex-grow": 4,
      "./flex-shrink": 5,
      "./flexbox-lines": 6,
      "./justify-content": 8,
      "./margin-cross": 9,
      "./margin-main": 10,
      "./order": 11
    }],
    8: [function (require, module, exports) {
      module.exports = function justifyContent(line, targetJustifyContent) {
        var start;
        var factor;

        if (targetJustifyContent === 'flex-start') {
          start = 0;

          line.children.forEach(function (child) {
            child.mainStart = start;

            start += child.mainAround;
          });
        } else if (targetJustifyContent === 'flex-end') {
          start = line.mainSpace;

          line.children.forEach(function (child) {
            child.mainStart = start;

            start += child.mainAround;
          });
        } else if (targetJustifyContent === 'center') {
          start = line.mainSpace / 2;

          line.children.forEach(function (child) {
            child.mainStart = start;

            start += child.mainAround;
          });
        } else if (targetJustifyContent === 'space-between') {
          factor = line.mainSpace / (line.children.length - 1);

          start = 0;

          line.children.forEach(function (child) {
            child.mainStart = start;

            start += child.mainAround + factor;
          });
        } else if (targetJustifyContent === 'space-around') {
          factor = line.mainSpace * 2 / (line.children.length * 2);
          start = factor / 2;

          line.children.forEach(function (child) {
            child.mainStart = start;

            start += child.mainAround + factor;
          });
        }
      };

    }, {}],
    9: [function (require, module, exports) {
      module.exports = function marginCross(line) {
        line.children.forEach(function (child) {
          var count = 0;

          if (child.crossBefore === 'auto') {
            ++count;
          }

          if (child.crossAfter === 'auto') {
            ++count;
          }

          var childSpace = line.cross - child.crossAround;

          if (child.crossBefore === 'auto') {
            child.crossBefore = childSpace / count;

            child.crossAround += child.crossBefore;
          }

          if (child.crossAfter === 'auto') {
            child.crossAfter = childSpace / count;

            child.crossAround += child.crossAfter;
          }
        });
      };

    }, {}],
    10: [function (require, module, exports) {
      module.exports = function marginCross(line) {
        var count = 0;

        line.children.forEach(function (child) {
          if (child.mainBefore === 'auto') {
            ++count;
          }

          if (child.mainAfter === 'auto') {
            ++count;
          }
        });

        if (count > 0) {
          line.children.forEach(function (child) {
            if (child.mainBefore === 'auto') {
              child.mainBefore = line.mainSpace / count;

              child.mainAround += child.mainBefore;
            }

            if (child.mainAfter === 'auto') {
              child.mainAfter = line.mainSpace / count;

              child.mainAround += child.mainAfter;
            }
          });

          line.mainSpace = 0;
        }
      };

    }, {}],
    11: [function (require, module, exports) {
      module.exports = function order(target) {
        target.children.sort(function (childA, childB) {
          return childA.order - childB.order || childA.index - childB.index;
        });
      };

    }, {}],
    12: [function (require, module, exports) {
      module.exports = function getFlexStyles(target, data, isFlexChild) {
        var style = Object.assign(data, {
          alignContent: 'stretch',
          alignItems: 'stretch',
          alignSelf: 'auto',
          display: 'inline',
          flexBasis: 'auto',
          flexDirection: 'row',
          flexGrow: 0,
          flexShrink: 1,
          flexWrap: 'nowrap',
          justifyContent: 'flex-start',
          height: 'auto',
          marginTop: 0,
          marginRight: 0,
          marginLeft: 0,
          marginBottom: 0,
          maxHeight: 'none',
          maxWidth: 'none',
          minHeight: 0,
          minWidth: 0,
          order: 0,
          position: 'static',
          width: 'auto'
        });

        if (target.hasAttribute('data-style')) {
          target.setAttribute('style', target.getAttribute('data-style'));
        } else {
          target.setAttribute('data-style', target.getAttribute('style') || '');
        }

        var attr = (target.getAttribute('data-style') || '') + ';' + (target.getAttribute('data-flex') || '');
        var re = /([^\s:;]+)\s*:\s*([^;]+?)\s*(;|$)/g;
        var decl;

        while (decl = re.exec(attr)) {
          var name = decl[1].toLowerCase().replace(/-[a-z]/g, function (match) {
            return match.slice(1).toUpperCase();
          });

          style[name] = parseFloat(decl[2]);

          if (isNaN(style[name])) {
            style[name] = decl[2];
          }
        }

        if (isFlexChild) {
          target.style.display = 'inline-block';
          target.style.position = 'absolute';
        }

        var rect = target.getBoundingClientRect();

        style.clientWidth = rect.width || target.offsetWidth;
        style.clientHeight = rect.height || target.offsetHeight;

        return style;
      };

    }, {}],
    13: [function (require, module, exports) {
      /*! Flexibility 2.0.0 | MIT Licensed | github.com/10up/flexibility */

      module.exports = function flexibility(target) {
        var data1 = module.exports.walk(target);

        var data2 = module.exports.flexbox(data1);

        var data3 = module.exports.write(data2);

        return data3;
      };

      module.exports.flexbox = require('./flexbox');
      module.exports.getFlexStyles = require('./getFlexStyles');
      module.exports.walk = require('./walk');
      module.exports.write = require('./write');

// module.exports.process = require('./process');
// module.exports.support = require('./support');

    }, {"./flexbox": 7, "./getFlexStyles": 12, "./walk": 14, "./write": 15}],
    14: [function (require, module, exports) {
      var getFlexStyles = require('../getFlexStyles');

      module.exports = function walk(target, ancestorData, isFlexChild) {
        var flexContainerRE = /(^|;)\s*display\s*:\s*(inline-)?flex\s*(;|$)/i;
        var isFlexContainer = flexContainerRE.test(target.getAttribute('data-flex'));
        var data = {
          node: target,
          children: [],
          descendants: []
        };

        if (isFlexContainer) {
          if (ancestorData !== undefined) {
            ancestorData.descendants.push(data);
          }
        }

        if (isFlexContainer || !ancestorData) {
          ancestorData = data;
        }

        Array.prototype.forEach.call(target.childNodes, function (childNode) {
          if (isFlexContainer && childNode.nodeType === 3 && childNode.nodeValue.trim()) {
            var oldNode = childNode;

            childNode = target.insertBefore(document.createElement('flex-item'), oldNode);

            childNode.appendChild(oldNode);
          }

          if (childNode.nodeType === 1) {
            var childData = module.exports(childNode, ancestorData, isFlexContainer);

            if (isFlexContainer) {
              data.children.push(childData);
            }
          }
        });

        if (isFlexContainer || isFlexChild) {
          getFlexStyles(target, data, isFlexChild);
        }

        return data;
      };

    }, {"../getFlexStyles": 12}],
    15: [function (require, module, exports) {
      module.exports = function write(target) {
        target.descendants.filter(function (descendant) {
          return target.children.indexOf(descendant) === -1;
        }).forEach(function (descendant) {
          module.exports(descendant);
        });

        if (!target.display) {
          return;
        }

        var style = target.node.style;

        if ('mainStart' in target) {
          style.position = 'absolute';

          if (target.mainAxis === 'inline') {
            style.left = target.mainStart + 'px';
            style.top = target.crossStart + 'px';

            style.marginTop = target.crossBefore + 'px';
            style.marginRight = target.mainAfter + 'px';
            style.marginBottom = target.crossAfter + 'px';
            style.marginLeft = target.mainBefore + 'px';
          } else {
            style.left = target.crossStart + 'px';
            style.top = target.mainStart + 'px';

            style.marginTop = target.mainBefore + 'px';
            style.marginRight = target.crossAfter + 'px';
            style.marginBottom = target.mainAfter + 'px';
            style.marginLeft = target.crossBefore + 'px';
          }

          if (target.mainAxis === 'inline') {
            style.width = target.mainAround - target.mainBefore - target.mainAfter + 'px';
            style.height = target.crossAround - target.crossBefore - target.crossAfter + 'px';
          } else {
            if (target.cross === 'auto') {
              style.width = target.crossClient - target.crossBefore - target.crossAfter + 'px';
            } else {
              style.width = target.crossAround - target.crossBefore - target.crossAfter + 'px';
            }

            if (target.main === 'auto') {
              style.height = target.mainClient - target.mainBefore - target.mainAfter + 'px';
            } else {
              style.height = target.mainAround - target.mainBefore - target.mainAfter + 'px';
            }
          }
        } else {
          if (!style.position) {
            style.position = 'relative';
          }

          if (target.mainAxis === 'inline') {
            style.width = target.mainAround - target.mainBefore - target.mainAfter + 'px';
            style.height = target.crossAround - target.crossBefore - target.crossAfter + 'px';
          } else {
            style.width = target.crossAround - target.crossBefore - target.crossAfter + 'px';
            style.height = target.mainAround - target.mainBefore - target.mainAfter + 'px';
          }
        }

        if (target.children) {
          target.children.forEach(function (child) {
            module.exports(child);
          });
        }
      };

    }, {}]
  }, {}, [13])(13)
});
/*! responsive-nav.js 1.0.39
 * https://github.com/viljamis/responsive-nav.js
 * http://responsive-nav.com
 *
 * Copyright (c) 2015 @viljamis
 * Available under the MIT license
 Licensed under the MIT license.

Copyright (c) 2013 Viljami Salminen, http://viljamis.com/

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

/* global Event */
(function (document, window, index) {
  // Index is used to keep multiple navs on the same page namespaced

  "use strict";

  var responsiveNav = function (el, options) {

    var computed = !!window.getComputedStyle;

    /**
     * getComputedStyle polyfill for old browsers
     */
    if (!computed) {
      window.getComputedStyle = function (el) {
        this.el = el;
        this.getPropertyValue = function (prop) {
          var re = /(\-([a-z]){1})/g;
          if (prop === "float") {
            prop = "styleFloat";
          }
          if (re.test(prop)) {
            prop = prop.replace(re, function () {
              return arguments[2].toUpperCase();
            });
          }
          return el.currentStyle[prop] ? el.currentStyle[prop] : null;
        };
        return this;
      };
    }
    /* exported addEvent, removeEvent, getChildren, setAttributes, addClass, removeClass, forEach */

    /**
     * Add Event
     * fn arg can be an object or a function, thanks to handleEvent
     * read more at: http://www.thecssninja.com/javascript/handleevent
     *
     * @param  {element}  element
     * @param  {event}    event
     * @param  {Function} fn
     * @param  {boolean}  bubbling
     */
    var addEvent = function (el, evt, fn, bubble) {
        if ("addEventListener" in el) {
          // BBOS6 doesn't support handleEvent, catch and polyfill
          try {
            el.addEventListener(evt, fn, bubble);
          } catch (e) {
            if (typeof fn === "object" && fn.handleEvent) {
              el.addEventListener(evt, function (e) {
                // Bind fn as this and set first arg as event object
                fn.handleEvent.call(fn, e);
              }, bubble);
            } else {
              throw e;
            }
          }
        } else if ("attachEvent" in el) {
          // check if the callback is an object and contains handleEvent
          if (typeof fn === "object" && fn.handleEvent) {
            el.attachEvent("on" + evt, function () {
              // Bind fn as this
              fn.handleEvent.call(fn);
            });
          } else {
            el.attachEvent("on" + evt, fn);
          }
        }
      },

      /**
       * Remove Event
       *
       * @param  {element}  element
       * @param  {event}    event
       * @param  {Function} fn
       * @param  {boolean}  bubbling
       */
      removeEvent = function (el, evt, fn, bubble) {
        if ("removeEventListener" in el) {
          try {
            el.removeEventListener(evt, fn, bubble);
          } catch (e) {
            if (typeof fn === "object" && fn.handleEvent) {
              el.removeEventListener(evt, function (e) {
                fn.handleEvent.call(fn, e);
              }, bubble);
            } else {
              throw e;
            }
          }
        } else if ("detachEvent" in el) {
          if (typeof fn === "object" && fn.handleEvent) {
            el.detachEvent("on" + evt, function () {
              fn.handleEvent.call(fn);
            });
          } else {
            el.detachEvent("on" + evt, fn);
          }
        }
      },

      /**
       * Get the children of any element
       *
       * @param  {element}
       * @return {array} Returns matching elements in an array
       */
      getChildren = function (e) {
        if (e.children.length < 1) {
          throw new Error("The Nav container has no containing elements");
        }
        // Store all children in array
        var children = [];
        // Loop through children and store in array if child != TextNode
        for (var i = 0; i < e.children.length; i++) {
          if (e.children[i].nodeType === 1) {
            children.push(e.children[i]);
          }
        }
        return children;
      },

      /**
       * Sets multiple attributes at once
       *
       * @param {element} element
       * @param {attrs}   attrs
       */
      setAttributes = function (el, attrs) {
        for (var key in attrs) {
          el.setAttribute(key, attrs[key]);
        }
      },

      /**
       * Adds a class to any element
       *
       * @param {element} element
       * @param {string}  class
       */
      addClass = function (el, cls) {
        if (el.className.indexOf(cls) !== 0) {
          el.className += " " + cls;
          el.className = el.className.replace(/(^\s*)|(\s*$)/g, "");
        }
      },

      /**
       * Remove a class from any element
       *
       * @param  {element} element
       * @param  {string}  class
       */
      removeClass = function (el, cls) {
        var reg = new RegExp("(\\s|^)" + cls + "(\\s|$)");
        el.className = el.className.replace(reg, " ").replace(/(^\s*)|(\s*$)/g, "");
      },

      /**
       * forEach method that passes back the stuff we need
       *
       * @param  {array}    array
       * @param  {Function} callback
       * @param  {scope}    scope
       */
      forEach = function (array, callback, scope) {
        for (var i = 0; i < array.length; i++) {
          callback.call(scope, i, array[i]);
        }
      };

    var nav,
      opts,
      navToggle,
      styleElement = document.createElement("style"),
      htmlEl = document.documentElement,
      hasAnimFinished,
      isMobile,
      navOpen;

    var ResponsiveNav = function (el, options) {
      var i;

      /**
       * Default options
       * @type {Object}
       */
      this.options = {
        animate: true,                    // Boolean: Use CSS3 transitions, true or false
        transition: 284,                  // Integer: Speed of the transition, in milliseconds
        label: "Menu",                    // String: Label for the navigation toggle
        insert: "before",                 // String: Insert the toggle before or after the navigation
        customToggle: "",                 // Selector: Specify the ID of a custom toggle
        closeOnNavClick: false,           // Boolean: Close the navigation when one of the links are clicked
        openPos: "relative",              // String: Position of the opened nav, relative or static
        navClass: "nav-collapse",         // String: Default CSS class. If changed, you need to edit the CSS too!
        navActiveClass: "js-nav-active",  // String: Class that is added to <html> element when nav is active
        jsClass: "js",                    // String: 'JS enabled' class which is added to <html> element
        init: function () {
        },               // Function: Init callback
        open: function () {
        },               // Function: Open callback
        close: function () {
        }               // Function: Close callback
      };

      // User defined options
      for (i in options) {
        this.options[i] = options[i];
      }

      // Adds "js" class for <html>
      addClass(htmlEl, this.options.jsClass);

      // Wrapper
      this.wrapperEl = el.replace("#", "");

      // Try selecting ID first
      if (document.getElementById(this.wrapperEl)) {
        this.wrapper = document.getElementById(this.wrapperEl);

        // If element with an ID doesn't exist, use querySelector
      } else if (document.querySelector(this.wrapperEl)) {
        this.wrapper = document.querySelector(this.wrapperEl);

        // If element doesn't exists, stop here.
      } else {
        throw new Error("The nav element you are trying to select doesn't exist");
      }

      // Inner wrapper
      this.wrapper.inner = getChildren(this.wrapper);

      // For minification
      opts = this.options;
      nav = this.wrapper;

      // Init
      this._init(this);
    };

    ResponsiveNav.prototype = {

      /**
       * Unattaches events and removes any classes that were added
       */
      destroy: function () {
        this._removeStyles();
        removeClass(nav, "closed");
        removeClass(nav, "opened");
        removeClass(nav, opts.navClass);
        removeClass(nav, opts.navClass + "-" + this.index);
        removeClass(htmlEl, opts.navActiveClass);
        nav.removeAttribute("style");
        nav.removeAttribute("aria-hidden");

        removeEvent(window, "resize", this, false);
        removeEvent(window, "focus", this, false);
        removeEvent(document.body, "touchmove", this, false);
        removeEvent(navToggle, "touchstart", this, false);
        removeEvent(navToggle, "touchend", this, false);
        removeEvent(navToggle, "mouseup", this, false);
        removeEvent(navToggle, "keyup", this, false);
        removeEvent(navToggle, "click", this, false);

        if (!opts.customToggle) {
          navToggle.parentNode.removeChild(navToggle);
        } else {
          navToggle.removeAttribute("aria-hidden");
        }
      },

      /**
       * Toggles the navigation open/close
       */
      toggle: function () {
        if (hasAnimFinished === true) {
          if (!navOpen) {
            this.open();
          } else {
            this.close();
          }
        }
      },

      /**
       * Opens the navigation
       */
      open: function () {
        if (!navOpen) {
          removeClass(nav, "closed");
          addClass(nav, "opened");
          addClass(htmlEl, opts.navActiveClass);
          addClass(navToggle, "active");
          nav.style.position = opts.openPos;
          setAttributes(nav, {"aria-hidden": "false"});
          navOpen = true;
          opts.open();
        }
      },

      /**
       * Closes the navigation
       */
      close: function () {
        if (navOpen) {
          addClass(nav, "closed");
          removeClass(nav, "opened");
          removeClass(htmlEl, opts.navActiveClass);
          removeClass(navToggle, "active");
          setAttributes(nav, {"aria-hidden": "true"});

          // If animations are enabled, wait until they finish
          if (opts.animate) {
            hasAnimFinished = false;
            setTimeout(function () {
              nav.style.position = "absolute";
              hasAnimFinished = true;
            }, opts.transition + 10);

            // Animations aren't enabled, we can do these immediately
          } else {
            nav.style.position = "absolute";
          }

          navOpen = false;
          opts.close();
        }
      },

      /**
       * Resize is called on window resize and orientation change.
       * It initializes the CSS styles and height calculations.
       */
      resize: function () {

        // Resize watches navigation toggle's display state
        if (window.getComputedStyle(navToggle, null).getPropertyValue("display") !== "none") {

          isMobile = true;
          setAttributes(navToggle, {"aria-hidden": "false"});

          // If the navigation is hidden
          if (nav.className.match(/(^|\s)closed(\s|$)/)) {
            setAttributes(nav, {"aria-hidden": "true"});
            nav.style.position = "absolute";
          }

          this._createStyles();
          this._calcHeight();
        } else {

          isMobile = false;
          setAttributes(navToggle, {"aria-hidden": "true"});
          setAttributes(nav, {"aria-hidden": "false"});
          nav.style.position = opts.openPos;
          this._removeStyles();
        }
      },

      /**
       * Takes care of all even handling
       *
       * @param  {event} event
       * @return {type} returns the type of event that should be used
       */
      handleEvent: function (e) {
        var evt = e || window.event;

        switch (evt.type) {
          case "touchstart":
            this._onTouchStart(evt);
            break;
          case "touchmove":
            this._onTouchMove(evt);
            break;
          case "touchend":
          case "mouseup":
            this._onTouchEnd(evt);
            break;
          case "click":
            this._preventDefault(evt);
            break;
          case "keyup":
            this._onKeyUp(evt);
            break;
          case "focus":
          case "resize":
            this.resize(evt);
            break;
        }
      },

      /**
       * Initializes the widget
       */
      _init: function () {
        this.index = index++;

        addClass(nav, opts.navClass);
        addClass(nav, opts.navClass + "-" + this.index);
        addClass(nav, "closed");
        hasAnimFinished = true;
        navOpen = false;

        this._closeOnNavClick();
        this._createToggle();
        this._transitions();
        this.resize();

        /**
         * On IE8 the resize event triggers too early for some reason
         * so it's called here again on init to make sure all the
         * calculated styles are correct.
         */
        var self = this;
        setTimeout(function () {
          self.resize();
        }, 20);

        addEvent(window, "resize", this, false);
        addEvent(window, "focus", this, false);
        addEvent(document.body, "touchmove", this, false);
        addEvent(navToggle, "touchstart", this, false);
        addEvent(navToggle, "touchend", this, false);
        addEvent(navToggle, "mouseup", this, false);
        addEvent(navToggle, "keyup", this, false);
        addEvent(navToggle, "click", this, false);

        /**
         * Init callback here
         */
        opts.init();
      },

      /**
       * Creates Styles to the <head>
       */
      _createStyles: function () {
        if (!styleElement.parentNode) {
          styleElement.type = "text/css";
          document.getElementsByTagName("head")[0].appendChild(styleElement);
        }
      },

      /**
       * Removes styles from the <head>
       */
      _removeStyles: function () {
        if (styleElement.parentNode) {
          styleElement.parentNode.removeChild(styleElement);
        }
      },

      /**
       * Creates Navigation Toggle
       */
      _createToggle: function () {

        // If there's no toggle, let's create one
        if (!opts.customToggle) {
          var toggle = document.createElement("a");
          toggle.innerHTML = opts.label;
          setAttributes(toggle, {
            "href": "#",
            "class": "nav-toggle"
          });

          // Determine where to insert the toggle
          if (opts.insert === "after") {
            nav.parentNode.insertBefore(toggle, nav.nextSibling);
          } else {
            nav.parentNode.insertBefore(toggle, nav);
          }

          navToggle = toggle;

          // There is a toggle already, let's use that one
        } else {
          var toggleEl = opts.customToggle.replace("#", "");

          if (document.getElementById(toggleEl)) {
            navToggle = document.getElementById(toggleEl);
          } else if (document.querySelector(toggleEl)) {
            navToggle = document.querySelector(toggleEl);
          } else {
            throw new Error("The custom nav toggle you are trying to select doesn't exist");
          }
        }
      },

      /**
       * Closes the navigation when a link inside is clicked.
       */
      _closeOnNavClick: function () {
        if (opts.closeOnNavClick) {
          var links = nav.getElementsByTagName("a"),
            self = this;
          forEach(links, function (i, el) {
            addEvent(links[i], "click", function () {
              if (isMobile) {
                self.toggle();
              }
            }, false);
          });
        }
      },

      /**
       * Prevents the default functionality.
       *
       * @param  {event} event
       */
      _preventDefault: function (e) {
        if (e.preventDefault) {
          if (e.stopImmediatePropagation) {
            e.stopImmediatePropagation();
          }
          e.preventDefault();
          e.stopPropagation();
          return false;

          // This is strictly for old IE
        } else {
          e.returnValue = false;
        }
      },

      /**
       * On touch start we get the location of the touch.
       *
       * @param  {event} event
       */
      _onTouchStart: function (e) {
        if (!Event.prototype.stopImmediatePropagation) {
          this._preventDefault(e);
        }
        this.startX = e.touches[0].clientX;
        this.startY = e.touches[0].clientY;
        this.touchHasMoved = false;

        /**
         * Remove mouseup event completely here to avoid
         * double triggering the event.
         */
        removeEvent(navToggle, "mouseup", this, false);
      },

      /**
       * Check if the user is scrolling instead of tapping.
       *
       * @param  {event} event
       */
      _onTouchMove: function (e) {
        if (Math.abs(e.touches[0].clientX - this.startX) > 10 ||
          Math.abs(e.touches[0].clientY - this.startY) > 10) {
          this.touchHasMoved = true;
        }
      },

      /**
       * On touch end toggle the navigation.
       *
       * @param  {event} event
       */
      _onTouchEnd: function (e) {
        this._preventDefault(e);
        if (!isMobile) {
          return;
        }

        // If the user isn't scrolling
        if (!this.touchHasMoved) {

          // If the event type is touch
          if (e.type === "touchend") {
            this.toggle();
            return;

            // Event type was click, not touch
          } else {
            var evt = e || window.event;

            // If it isn't a right click, do toggling
            if (!(evt.which === 3 || evt.button === 2)) {
              this.toggle();
            }
          }
        }
      },

      /**
       * For keyboard accessibility, toggle the navigation on Enter
       * keypress too.
       *
       * @param  {event} event
       */
      _onKeyUp: function (e) {
        var evt = e || window.event;
        if (evt.keyCode === 13) {
          this.toggle();
        }
      },

      /**
       * Adds the needed CSS transitions if animations are enabled
       */
      _transitions: function () {
        if (opts.animate) {
          var objStyle = nav.style,
            transition = "max-height " + opts.transition + "ms";

          objStyle.WebkitTransition =
            objStyle.MozTransition =
              objStyle.OTransition =
                objStyle.transition = transition;
        }
      },

      /**
       * Calculates the height of the navigation and then creates
       * styles which are later added to the page <head>
       */
      _calcHeight: function () {
        var savedHeight = 0;
        for (var i = 0; i < nav.inner.length; i++) {
          savedHeight += nav.inner[i].offsetHeight;
        }

        var innerStyles = "." + opts.jsClass + " ." + opts.navClass + "-" + this.index + ".opened{max-height:" + savedHeight + "px !important} ." + opts.jsClass + " ." + opts.navClass + "-" + this.index + ".opened.dropdown-active {max-height:9999px !important}";

        if (styleElement.styleSheet) {
          styleElement.styleSheet.cssText = innerStyles;
        } else {
          styleElement.innerHTML = innerStyles;
        }

        innerStyles = "";
      }

    };

    /**
     * Return new Responsive Nav
     */
    return new ResponsiveNav(el, options);

  };

  if (typeof module !== "undefined" && module.exports) {
    module.exports = responsiveNav;
  } else {
    window.responsiveNav = responsiveNav;
  }

}(document, window, 0));

document.addEventListener("DOMContentLoaded", function () {
  window.pageYOffset || document.documentElement.scrollTop;

  function e(e, t) {
    if (e) {
      "string" == typeof e ? e = document.querySelectorAll(e) : e.tagName && (e = [e]);
      for (var n = 0; n < e.length; n++) (" " + e[n].className + " ").indexOf(" " + t + " ") < 0 && (e[n].className += " " + t)
    }
  }

  function t(e, t) {
    if (e) {
      "string" == typeof e ? e = document.querySelectorAll(e) : e.tagName && (e = [e]);
      for (var n = new RegExp("(^| )" + t + "($| )", "g"), o = 0; o < e.length; o++) e[o].className = e[o].className.replace(n, " ")
    }
  }

  if (window.onresize = function (e) {
    window.pageYOffset || document.documentElement.scrollTop
  }, "querySelector" in document && "addEventListener" in window && Array.prototype.forEach) {
    var n = document.querySelectorAll(".scroll");
    [].forEach.call(n, function (o) {
      o.addEventListener("click", function (e) {
        e.preventDefault();
        var t = document.querySelector(".landing__section"),
          n = o.getAttribute("data-speed");
        t && function (e, t) {
          var n, o = window.pageYOffset,
            r = e.offsetTop - 40,
            i = (r - o) / (t / 16);
          0 <= i && (n = function () {
            var e = window.pageYOffset;
            (r - i <= e || window.innerHeight + e >= document.body.offsetHeight) && clearInterval(s)
          });
          var s = setInterval(function () {
            window.scrollBy(0, i), n()
          }, 16)
        }(t, n || 700)
      }, !1)
    })
  }
  if (window.addEventListener("scroll", function () {
    document.body.contains(document.getElementById("navConverter")) && ((window.pageYOffset || document.documentElement.scrollTop) > function (e) {
      for (var t = 0, n = 0; e && !isNaN(e.offsetLeft) && !isNaN(e.offsetTop);) t += e.offsetLeft - e.scrollLeft, n += e.offsetTop - e.scrollTop, e = e.offsetParent;
      return {
        top: n,
        left: t
      }
    }(document.getElementById("navConverter")).top - 60 ? t(document.querySelector(".navbar"), "navbar--extended") : e(document.querySelector(".navbar"), "navbar--extended"));
    document.body.contains(document.getElementById("scrollToNext")) && (20 < (window.pageYOffset || document.documentElement.scrollTop) ? e(document.getElementById("scrollToNext"), "invisible") : t(document.getElementById("scrollToNext"), "invisible"))
  }), document.getElementsByClassName("nav__mobile") && 0 < document.getElementsByClassName("nav__mobile").length) {
    var o = document.getElementsByClassName("navbar__menu")[0].innerHTML;
    document.getElementsByClassName("nav__mobile")[0].innerHTML = o;
    responsiveNav(".nav__mobile", {
      animate: !0,
      transition: 284,
      label: "Menu",
      insert: "before",
      customToggle: "toggle",
      openPos: "relative",
      navClass: "nav__mobile"
    })
  } else e(document.querySelector(".navbar__menu"), "navbar__menu--noMob"), e(document.querySelector(".navbar__menu-mob"), "navbar__menu-mob--noMob")
}),
  function (e) {
    if ("object" == typeof exports && "undefined" != typeof module) module.exports = e();
    else if ("function" == typeof define && define.amd) define([], e);
    else {
      ("undefined" != typeof window ? window : "undefined" != typeof global ? global : "undefined" != typeof self ? self : this).flexibility = e()
    }
  }(function () {
    return function i(s, a, c) {
      function l(n, e) {
        if (!a[n]) {
          if (!s[n]) {
            var t = "function" == typeof require && require;
            if (!e && t) return t(n, !0);
            if (f) return f(n, !0);
            var o = new Error("Cannot find module '" + n + "'");
            throw o.code = "MODULE_NOT_FOUND", o
          }
          var r = a[n] = {
            exports: {}
          };
          s[n][0].call(r.exports, function (e) {
            var t = s[n][1][e];
            return l(t || e)
          }, r, r.exports, i, s, a, c)
        }
        return a[n].exports
      }

      for (var f = "function" == typeof require && require, e = 0; e < c.length; e++) l(c[e]);
      return l
    }({
      1: [function (e, t, n) {
        t.exports = function (e) {
          var t, n;
          e.lines.length < 2 || "stretch" === e.alignContent ? (n = e.crossSpace / e.lines.length, t = 0, e.lines.forEach(function (e) {
            e.crossStart = t, e.cross += n, t += e.cross
          })) : "flex-start" === e.alignContent ? (t = 0, e.lines.forEach(function (e) {
            e.crossStart = t, t += e.cross
          })) : "flex-end" === e.alignContent ? (t = e.crossSpace, e.lines.forEach(function (e) {
            e.crossStart = t, t += e.cross
          })) : "center" === e.alignContent ? (t = e.crossSpace / 2, e.lines.forEach(function (e) {
            e.crossStart = t, t += e.cross
          })) : "space-between" === e.alignContent ? (n = e.crossSpace / (e.lines.length - 1), t = 0, e.lines.forEach(function (e) {
            e.crossStart = t, t += e.cross + n
          })) : "space-around" === e.alignContent ? (n = 2 * e.crossSpace / (2 * e.lines.length), t = n / 2, e.lines.forEach(function (e) {
            e.crossStart = t, t += e.cross + n
          })) : "stretch" === e.alignContent && (n = e.crossSpace / e.lines.length, t = 0, e.lines.forEach(function (e) {
            e.crossStart = t, e.cross += n, t += e.cross
          }))
        }
      }, {}],
      2: [function (e, t, n) {
        t.exports = function (e) {
          e.lines.forEach(function (t) {
            t.children.forEach(function (e) {
              "flex-start" === e.alignSelf ? e.crossStart = t.crossStart : "flex-end" === e.alignSelf ? e.crossStart = t.crossStart + t.cross - e.crossAround : "center" === e.alignSelf ? e.crossStart = t.crossStart + (t.cross - e.crossAround) / 2 : "stretch" === e.alignSelf && (e.crossStart = t.crossStart, e.crossAround = t.cross)
            })
          })
        }
      }, {}],
      3: [function (e, t, n) {
        t.exports = function (e, t, n) {
          var o = e.node.getBoundingClientRect();
          e.crossAfter = "row" === t || "row-reverse" === t ? (e.mainAxis = "inline", e.crossAxis = "block", "number" != typeof e.main && "number" != typeof e.cross || ("row" === e.flexDirection || "row-reverse" === t ? (e.width = e.main, e.height = e.cross) : (e.width = e.cross, e.height = e.main)), e.main = e.width, e.cross = e.height, e.mainClient = o.width || e.node.offsetWidth, e.crossClient = o.height || e.node.offsetHeight, e.mainBefore = e.marginLeft, e.mainAfter = e.marginRight, e.crossBefore = e.marginTop, e.marginBottom) : (e.mainAxis = "block", e.crossAxis = "inline", e.main = e.height, e.cross = e.width, "number" != typeof e.main && "number" != typeof e.cross || ("column" === e.flexDirection || "column-reverse" === t ? (e.width = e.cross, e.height = e.main) : (e.width = e.main, e.height = e.cross)), e.mainClient = o.height || e.node.offsetHeight, e.crossClient = o.width || e.node.offsetWidth, e.mainBefore = e.marginTop, e.mainAfter = e.marginBottom, e.crossBefore = e.marginLeft, e.marginRight), "number" == typeof e.flexBasis && (e.main = e.flexBasis), "auto" === e.main ? e.mainAround = e.mainClient : e.mainAround = e.main, "auto" === e.cross ? e.crossAround = e.crossClient : e.crossAround = e.cross, "number" == typeof e.mainBefore && (e.mainAround += e.mainBefore), "number" == typeof e.mainAfter && (e.mainAround += e.mainAfter), "number" == typeof e.crossBefore && (e.crossAround += e.crossBefore), "number" == typeof e.crossBefore && (e.crossAround += e.crossBefore), "auto" === e.alignSelf && (e.alignSelf = n)
        }
      }, {}],
      4: [function (e, t, n) {
        t.exports = function (t) {
          if (0 < t.mainSpace) {
            var n = t.children.reduce(function (e, t) {
              return e + t.flexGrow
            }, 0);
            0 < n && (t.children.forEach(function (e) {
              e.mainAround += e.flexGrow / n * t.mainSpace
            }), t.main = t.children.reduce(function (e, t) {
              return e + t.mainAround
            }, 0), t.mainSpace = 0)
          }
        }
      }, {}],
      5: [function (e, t, n) {
        t.exports = function (t) {
          if (t.mainSpace < 0) {
            var n = t.children.reduce(function (e, t) {
              return e + t.flexShrink
            }, 0);
            0 < n && (t.children.forEach(function (e) {
              e.mainAround += e.flexShrink / n * t.mainSpace
            }), t.main = t.children.reduce(function (e, t) {
              return e + t.mainAround
            }, 0), t.mainSpace = 0)
          }
        }
      }, {}],
      6: [function (e, t, n) {
        t.exports = function (t) {
          var n;
          t.lines = [n = {
            main: 0,
            cross: 0,
            children: []
          }], t.children.forEach(function (e) {
            "nowrap" === t.flexWrap || 0 === n.children.length || t.mainAround >= n.main + e.mainAround ? (n.main += e.mainAround, n.cross = Math.max(n.cross, e.crossAround)) : t.lines.push(n = {
              main: e.mainAround,
              cross: e.crossAround,
              children: []
            }), n.children.push(e)
          })
        }
      }, {}],
      7: [function (n, o, e) {
        o.exports = function (t) {
          return t.descendants.forEach(function (e) {
            o.exports(e)
          }), "flex" !== t.display || (t.children.forEach(function (e) {
            n("./flex-direction")(e, t.flexDirection, t.alignItems)
          }), n("./order")(t), n("./flex-direction")(t, t.flexDirection, t.alignItems), n("./flexbox-lines")(t), "auto" === t.main && (t.main = Math.max(t.mainAround, t.lines.reduce(function (e, t) {
            return Math.max(e, t.main)
          }, 0)), "row" === t.flexDirection ? t.mainAround = t.mainClient + t.mainBefore + t.mainAfter : t.mainAround = t.main + t.mainBefore + t.mainAfter), "auto" === t.cross ? (t.cross = t.lines.reduce(function (e, t) {
            return e + t.cross
          }, 0), "column" === t.flexDirection ? t.crossAround = t.crossClient + t.crossBefore + t.crossAfter : t.crossAround = t.cross + t.crossBefore + t.crossAfter, t.crossSpace = t.crossAround - t.cross) : t.crossSpace = t.cross - t.lines.reduce(function (e, t) {
            return e + t.cross
          }, 0), n("./align-content")(t), t.lines.forEach(function (e) {
            e.mainSpace = t.main - e.main, n("./flex-grow")(e), n("./flex-shrink")(e), n("./margin-main")(e), n("./margin-cross")(e), n("./justify-content")(e, t.justifyContent)
          }), n("./align-items")(t)), t
        }
      }, {
        "./align-content": 1,
        "./align-items": 2,
        "./flex-direction": 3,
        "./flex-grow": 4,
        "./flex-shrink": 5,
        "./flexbox-lines": 6,
        "./justify-content": 8,
        "./margin-cross": 9,
        "./margin-main": 10,
        "./order": 11
      }],
      8: [function (e, t, n) {
        t.exports = function (e, t) {
          var n, o;
          "flex-start" === t ? (n = 0, e.children.forEach(function (e) {
            e.mainStart = n, n += e.mainAround
          })) : "flex-end" === t ? (n = e.mainSpace, e.children.forEach(function (e) {
            e.mainStart = n, n += e.mainAround
          })) : "center" === t ? (n = e.mainSpace / 2, e.children.forEach(function (e) {
            e.mainStart = n, n += e.mainAround
          })) : "space-between" === t ? (o = e.mainSpace / (e.children.length - 1), n = 0, e.children.forEach(function (e) {
            e.mainStart = n, n += e.mainAround + o
          })) : "space-around" === t && (o = 2 * e.mainSpace / (2 * e.children.length), n = o / 2, e.children.forEach(function (e) {
            e.mainStart = n, n += e.mainAround + o
          }))
        }
      }, {}],
      9: [function (e, t, n) {
        t.exports = function (o) {
          o.children.forEach(function (e) {
            var t = 0;
            "auto" === e.crossBefore && ++t, "auto" === e.crossAfter && ++t;
            var n = o.cross - e.crossAround;
            "auto" === e.crossBefore && (e.crossBefore = n / t, e.crossAround += e.crossBefore), "auto" === e.crossAfter && (e.crossAfter = n / t, e.crossAround += e.crossAfter)
          })
        }
      }, {}],
      10: [function (e, t, n) {
        t.exports = function (t) {
          var n = 0;
          t.children.forEach(function (e) {
            "auto" === e.mainBefore && ++n, "auto" === e.mainAfter && ++n
          }), 0 < n && (t.children.forEach(function (e) {
            "auto" === e.mainBefore && (e.mainBefore = t.mainSpace / n, e.mainAround += e.mainBefore), "auto" === e.mainAfter && (e.mainAfter = t.mainSpace / n, e.mainAround += e.mainAfter)
          }), t.mainSpace = 0)
        }
      }, {}],
      11: [function (e, t, n) {
        t.exports = function (e) {
          e.children.sort(function (e, t) {
            return e.order - t.order || e.index - t.index
          })
        }
      }, {}],
      12: [function (e, t, n) {
        t.exports = function (e, t, n) {
          var o = Object.assign(t, {
            alignContent: "stretch",
            alignItems: "stretch",
            alignSelf: "auto",
            display: "inline",
            flexBasis: "auto",
            flexDirection: "row",
            flexGrow: 0,
            flexShrink: 1,
            flexWrap: "nowrap",
            justifyContent: "flex-start",
            height: "auto",
            marginTop: 0,
            marginRight: 0,
            marginLeft: 0,
            marginBottom: 0,
            maxHeight: "none",
            maxWidth: "none",
            minHeight: 0,
            minWidth: 0,
            order: 0,
            position: "static",
            width: "auto"
          });
          e.hasAttribute("data-style") ? e.setAttribute("style", e.getAttribute("data-style")) : e.setAttribute("data-style", e.getAttribute("style") || "");
          for (var r, i = (e.getAttribute("data-style") || "") + ";" + (e.getAttribute("data-flex") || ""), s = /([^\s:;]+)\s*:\s*([^;]+?)\s*(;|$)/g; r = s.exec(i);) {
            var a = r[1].toLowerCase().replace(/-[a-z]/g, function (e) {
              return e.slice(1).toUpperCase()
            });
            o[a] = parseFloat(r[2]), isNaN(o[a]) && (o[a] = r[2])
          }
          n && (e.style.display = "inline-block", e.style.position = "absolute");
          var c = e.getBoundingClientRect();
          return o.clientWidth = c.width || e.offsetWidth, o.clientHeight = c.height || e.offsetHeight, o
        }
      }, {}],
      13: [function (e, o, t) {
        o.exports = function (e) {
          var t = o.exports.walk(e),
            n = o.exports.flexbox(t);
          return o.exports.write(n)
        }, o.exports.flexbox = e("./flexbox"), o.exports.getFlexStyles = e("./getFlexStyles"), o.exports.walk = e("./walk"), o.exports.write = e("./write")
      }, {
        "./flexbox": 7,
        "./getFlexStyles": 12,
        "./walk": 14,
        "./write": 15
      }],
      14: [function (e, a, t) {
        var n = e("../getFlexStyles");
        a.exports = function (o, r, e) {
          var i = /(^|;)\s*display\s*:\s*(inline-)?flex\s*(;|$)/i.test(o.getAttribute("data-flex")),
            s = {
              node: o,
              children: [],
              descendants: []
            };
          return i && void 0 !== r && r.descendants.push(s), !i && r || (r = s), Array.prototype.forEach.call(o.childNodes, function (e) {
            if (i && 3 === e.nodeType && e.nodeValue.trim()) {
              var t = e;
              (e = o.insertBefore(document.createElement("flex-item"), t)).appendChild(t)
            }
            if (1 === e.nodeType) {
              var n = a.exports(e, r, i);
              i && s.children.push(n)
            }
          }), (i || e) && n(o, s, e), s
        }
      }, {
        "../getFlexStyles": 12
      }],
      15: [function (e, n, t) {
        n.exports = function (t) {
          if (t.descendants.filter(function (e) {
            return -1 === t.children.indexOf(e)
          }).forEach(function (e) {
            n.exports(e)
          }), t.display) {
            var e = t.node.style;
            "mainStart" in t ? (e.position = "absolute", "inline" === t.mainAxis ? (e.left = t.mainStart + "px", e.top = t.crossStart + "px", e.marginTop = t.crossBefore + "px", e.marginRight = t.mainAfter + "px", e.marginBottom = t.crossAfter + "px", e.marginLeft = t.mainBefore + "px") : (e.left = t.crossStart + "px", e.top = t.mainStart + "px", e.marginTop = t.mainBefore + "px", e.marginRight = t.crossAfter + "px", e.marginBottom = t.mainAfter + "px", e.marginLeft = t.crossBefore + "px"), "inline" === t.mainAxis ? (e.width = t.mainAround - t.mainBefore - t.mainAfter + "px", e.height = t.crossAround - t.crossBefore - t.crossAfter + "px") : ("auto" === t.cross ? e.width = t.crossClient - t.crossBefore - t.crossAfter + "px" : e.width = t.crossAround - t.crossBefore - t.crossAfter + "px", "auto" === t.main ? e.height = t.mainClient - t.mainBefore - t.mainAfter + "px" : e.height = t.mainAround - t.mainBefore - t.mainAfter + "px")) : (e.position || (e.position = "relative"), "inline" === t.mainAxis ? (e.width = t.mainAround - t.mainBefore - t.mainAfter + "px", e.height = t.crossAround - t.crossBefore - t.crossAfter + "px") : (e.width = t.crossAround - t.crossBefore - t.crossAfter + "px", e.height = t.mainAround - t.mainBefore - t.mainAfter + "px")), t.children && t.children.forEach(function (e) {
              n.exports(e)
            })
          }
        }
      }, {}]
    }, {}, [13])(13)
  }),
  function (g, v, x) {
    "use strict";
    var e = function (e, t) {
      !!v.getComputedStyle || (v.getComputedStyle = function (n) {
        return this.el = n, this.getPropertyValue = function (e) {
          var t = /(\-([a-z]){1})/g;
          return "float" === e && (e = "styleFloat"), t.test(e) && (e = e.replace(t, function () {
            return arguments[2].toUpperCase()
          })), n.currentStyle[e] ? n.currentStyle[e] : null
        }, this
      });
      var r, i, n, o, s, a, c = function (t, n, o, r) {
          if ("addEventListener" in t) try {
            t.addEventListener(n, o, r)
          } catch (e) {
            if ("object" != typeof o || !o.handleEvent) throw e;
            t.addEventListener(n, function (e) {
              o.handleEvent.call(o, e)
            }, r)
          } else "attachEvent" in t && ("object" == typeof o && o.handleEvent ? t.attachEvent("on" + n, function () {
            o.handleEvent.call(o)
          }) : t.attachEvent("on" + n, o))
        },
        l = function (t, n, o, r) {
          if ("removeEventListener" in t) try {
            t.removeEventListener(n, o, r)
          } catch (e) {
            if ("object" != typeof o || !o.handleEvent) throw e;
            t.removeEventListener(n, function (e) {
              o.handleEvent.call(o, e)
            }, r)
          } else "detachEvent" in t && ("object" == typeof o && o.handleEvent ? t.detachEvent("on" + n, function () {
            o.handleEvent.call(o)
          }) : t.detachEvent("on" + n, o))
        },
        f = function (e, t) {
          for (var n in t) e.setAttribute(n, t[n])
        },
        u = function (e, t) {
          0 !== e.className.indexOf(t) && (e.className += " " + t, e.className = e.className.replace(/(^\s*)|(\s*$)/g, ""))
        },
        d = function (e, t) {
          var n = new RegExp("(\\s|^)" + t + "(\\s|$)");
          e.className = e.className.replace(n, " ").replace(/(^\s*)|(\s*$)/g, "")
        },
        m = g.createElement("style"),
        h = g.documentElement,
        p = function (e, t) {
          var n;
          for (n in this.options = {
            animate: !0,
            transition: 284,
            label: "Menu",
            insert: "before",
            customToggle: "",
            closeOnNavClick: !1,
            openPos: "relative",
            navClass: "nav-collapse",
            navActiveClass: "js-nav-active",
            jsClass: "js",
            init: function () {
            },
            open: function () {
            },
            close: function () {
            }
          }, t) this.options[n] = t[n];
          if (u(h, this.options.jsClass), this.wrapperEl = e.replace("#", ""), g.getElementById(this.wrapperEl)) this.wrapper = g.getElementById(this.wrapperEl);
          else {
            if (!g.querySelector(this.wrapperEl)) throw new Error("The nav element you are trying to select doesn't exist");
            this.wrapper = g.querySelector(this.wrapperEl)
          }
          this.wrapper.inner = function (e) {
            if (e.children.length < 1) throw new Error("The Nav container has no containing elements");
            for (var t = [], n = 0; n < e.children.length; n++) 1 === e.children[n].nodeType && t.push(e.children[n]);
            return t
          }(this.wrapper), i = this.options, r = this.wrapper, this._init(this)
        };
      return p.prototype = {
        destroy: function () {
          this._removeStyles(), d(r, "closed"), d(r, "opened"), d(r, i.navClass), d(r, i.navClass + "-" + this.index), d(h, i.navActiveClass), r.removeAttribute("style"), r.removeAttribute("aria-hidden"), l(v, "resize", this, !1), l(v, "focus", this, !1), l(g.body, "touchmove", this, !1), l(n, "touchstart", this, !1), l(n, "touchend", this, !1), l(n, "mouseup", this, !1), l(n, "keyup", this, !1), l(n, "click", this, !1), i.customToggle ? n.removeAttribute("aria-hidden") : n.parentNode.removeChild(n)
        },
        toggle: function () {
          !0 === o && (a ? this.close() : this.open())
        },
        open: function () {
          a || (d(r, "closed"), u(r, "opened"), u(h, i.navActiveClass), u(n, "active"), r.style.position = i.openPos, f(r, {
            "aria-hidden": "false"
          }), a = !0, i.open())
        },
        close: function () {
          a && (u(r, "closed"), d(r, "opened"), d(h, i.navActiveClass), d(n, "active"), f(r, {
            "aria-hidden": "true"
          }), i.animate ? (o = !1, setTimeout(function () {
            r.style.position = "absolute", o = !0
          }, i.transition + 10)) : r.style.position = "absolute", a = !1, i.close())
        },
        resize: function () {
          "none" !== v.getComputedStyle(n, null).getPropertyValue("display") ? (s = !0, f(n, {
            "aria-hidden": "false"
          }), r.className.match(/(^|\s)closed(\s|$)/) && (f(r, {
            "aria-hidden": "true"
          }), r.style.position = "absolute"), this._createStyles(), this._calcHeight()) : (s = !1, f(n, {
            "aria-hidden": "true"
          }), f(r, {
            "aria-hidden": "false"
          }), r.style.position = i.openPos, this._removeStyles())
        },
        handleEvent: function (e) {
          var t = e || v.event;
          switch (t.type) {
            case "touchstart":
              this._onTouchStart(t);
              break;
            case "touchmove":
              this._onTouchMove(t);
              break;
            case "touchend":
            case "mouseup":
              this._onTouchEnd(t);
              break;
            case "click":
              this._preventDefault(t);
              break;
            case "keyup":
              this._onKeyUp(t);
              break;
            case "focus":
            case "resize":
              this.resize(t)
          }
        },
        _init: function () {
          this.index = x++, u(r, i.navClass), u(r, i.navClass + "-" + this.index), u(r, "closed"), a = !(o = !0), this._closeOnNavClick(), this._createToggle(), this._transitions(), this.resize();
          var e = this;
          setTimeout(function () {
            e.resize()
          }, 20), c(v, "resize", this, !1), c(v, "focus", this, !1), c(g.body, "touchmove", this, !1), c(n, "touchstart", this, !1), c(n, "touchend", this, !1), c(n, "mouseup", this, !1), c(n, "keyup", this, !1), c(n, "click", this, !1), i.init()
        },
        _createStyles: function () {
          m.parentNode || (m.type = "text/css", g.getElementsByTagName("head")[0].appendChild(m))
        },
        _removeStyles: function () {
          m.parentNode && m.parentNode.removeChild(m)
        },
        _createToggle: function () {
          if (i.customToggle) {
            var e = i.customToggle.replace("#", "");
            if (g.getElementById(e)) n = g.getElementById(e);
            else {
              if (!g.querySelector(e)) throw new Error("The custom nav toggle you are trying to select doesn't exist");
              n = g.querySelector(e)
            }
          } else {
            var t = g.createElement("a");
            t.innerHTML = i.label, f(t, {
              href: "#",
              class: "nav-toggle"
            }), "after" === i.insert ? r.parentNode.insertBefore(t, r.nextSibling) : r.parentNode.insertBefore(t, r), n = t
          }
        },
        _closeOnNavClick: function () {
          if (i.closeOnNavClick) {
            var n = r.getElementsByTagName("a"),
              o = this;
            !function (e, t, n) {
              for (var o = 0; o < e.length; o++) t.call(n, o, e[o])
            }(n, function (e, t) {
              c(n[e], "click", function () {
                s && o.toggle()
              }, !1)
            })
          }
        },
        _preventDefault: function (e) {
          if (e.preventDefault) return e.stopImmediatePropagation && e.stopImmediatePropagation(), e.preventDefault(), e.stopPropagation(), !1;
          e.returnValue = !1
        },
        _onTouchStart: function (e) {
          Event.prototype.stopImmediatePropagation || this._preventDefault(e), this.startX = e.touches[0].clientX, this.startY = e.touches[0].clientY, this.touchHasMoved = !1, l(n, "mouseup", this, !1)
        },
        _onTouchMove: function (e) {
          (10 < Math.abs(e.touches[0].clientX - this.startX) || 10 < Math.abs(e.touches[0].clientY - this.startY)) && (this.touchHasMoved = !0)
        },
        _onTouchEnd: function (e) {
          if (this._preventDefault(e), s && !this.touchHasMoved) {
            if ("touchend" === e.type) return void this.toggle();
            var t = e || v.event;
            3 !== t.which && 2 !== t.button && this.toggle()
          }
        },
        _onKeyUp: function (e) {
          13 === (e || v.event).keyCode && this.toggle()
        },
        _transitions: function () {
          if (i.animate) {
            var e = r.style,
              t = "max-height " + i.transition + "ms";
            e.WebkitTransition = e.MozTransition = e.OTransition = e.transition = t
          }
        },
        _calcHeight: function () {
          for (var e = 0, t = 0; t < r.inner.length; t++) e += r.inner[t].offsetHeight;
          var n = "." + i.jsClass + " ." + i.navClass + "-" + this.index + ".opened{max-height:" + e + "px !important} ." + i.jsClass + " ." + i.navClass + "-" + this.index + ".opened.dropdown-active {max-height:9999px !important}";
          m.styleSheet ? m.styleSheet.cssText = n : m.innerHTML = n, n = ""
        }
      }, new p(e, t)
    };
    "undefined" != typeof module && module.exports ? module.exports = e : v.responsiveNav = e
  }(document, window, 0);
