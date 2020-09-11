import functools

HIGHLIGHT_COLORS = [
    "blue",
    "green",
    "pink",
    "orange",
    "purple",
    "teal",
    "tan",
    "red",
    "cobalt",
    "brown",
    "slate",
    "fuchsia",
    "gray"
]

def get_highlight_color(index):
    if index <= len(HIGHLIGHT_COLORS):
        return HIGHLIGHT_COLORS[index]
    else:
        return HIGHLIGHT_COLORS[index - (len(HIGHLIGHT_COLORS) * math.floor(index / len(HIGHLIGHT_COLORS)))]

# Transofrms tokens and clusters into a tree representation
def transform_to_tree(tokens, clusters):
    def contains(span, index):
        return index >= span[0] and index <= span[1]


    inside_clusters = [{
        'cluster': -1,
        'contents': [],
        'end': -1
    }]

    for i, token in enumerate(tokens):
        # Find all the new clusters we are entering at the current index
        new_clusters = []
        for j, cluster in enumerate(clusters):
            #Make sure we're not already in this cluster
            if j not in [c['cluster'] for c in inside_clusters]:
                for span in cluster:
                    if i in span:
                        new_clusters.append({ 'end': span[1], 'cluster': j })

        # Enter each new cluster, starting with the leftmost
        new_clusters = sorted(new_clusters, key=functools.cmp_to_key(lambda a, b: b['end'] - a['end']))
        for new_cluster in new_clusters:
            #Descend into the new cluster
            inside_clusters.append({
                'cluster': new_cluster['cluster'],
                'contents': [],
                'end': new_cluster['end']
            })

        #Add the current token into the current cluster
        inside_clusters[-1]['contents'].append(token)

        # Exit each cluster we're at the end of
        while (len(inside_clusters) > 0 and inside_clusters[-1]['end'] == i):
            top_cluster = inside_clusters[-1]
            inside_clusters.pop()
            inside_clusters[-1]['contents'].append(top_cluster)

    yoohoo = inside_clusters[0]['contents']
    my_clusters = []
    for yoo in yoohoo:
      # print ("{} has type {}".format(yoo, type(yoo)))
      if isinstance(yoo, dict):
        my_clusters.append(yoo)

    # print ("we should be returning {}".format(yoohoo))
    return [yoohoo, my_clusters]


#This is the function that calls itself when we recurse over the span tree.
def gen_elem(token, idx, depth, to_html):
    if to_html:
        if isinstance(token, dict) or isinstance(token, list):
            return '<span key={} class="highlight {}" depth={} id={} onmouseover="handleHighlightMouseOver(this)" \
                    onmouseout="handleHighlightMouseOut(this)" labelPosition="left">\
                    <span class="highlight__label"><strong>{}</strong></span>\
                    <span class="highlight__content">{}</span></span>'.format(idx, 
                                                                              get_highlight_color(token['cluster']), 
                                                                              depth,
                                                                              token['cluster'],
                                                                              token['cluster'], 
                                                                              ' '.join(span_wrapper(token['contents'], depth + 1, to_html)))
        else:
            return '<span>{} </span>'.format(token)

    else:
        if isinstance(token, dict) or isinstance(token, list):
        
            return "[{}: {}]".format(token['cluster'],
                                                ' '.join(span_wrapper(token['contents'], depth + 1, to_html)))
        else:
            return " {} ".format(token)
 
# Wraps the tree representation into spans indicating cluster-wise depth
def span_wrapper(tree, depth, to_html):
      stuff = [gen_elem(token, idx, depth, to_html) for idx, token in enumerate(tree)]
      # print ("span_wrapper is about to return {}".format(stuff)) 
      return stuff
