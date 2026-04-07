import numpy as np
import math

def enforce_viewpoint_consistency(centroid, U, V, W, viewpoint=(0,0,30)):
    # Get vector from point to viewpoint (camera)
    to_view = viewpoint - centroid
    # Normalize
    to_view = to_view / np.linalg.norm(to_view)
    # Get dot product of that with W
    dot_val = np.dot(to_view, W)
    # If negative, flip
    if dot_val < 0:
        W = -W
        
    # Return results
    return U, V, W

def compute_distances(center, points): # sqrt((x2 - x1) ^ 2 + (y2 - y1) ^ 2 + (z2 - z1) ^ 2)
    Eu_Dist = []

    for Items in points:
        temp_x = center[0] - Items[0]
        temp_x = temp_x * temp_x

        temp_y = center[1] - Items[1]
        temp_y = temp_y * temp_y

        temp_z = center[2] - Items[2]
        temp_z = temp_z * temp_z

        Eu_Dist.append(math.sqrt(temp_x + temp_y + temp_z))

    return Eu_Dist

def compute_gaussian_weights(center, points, sigma):    # E ^ (Dist ^ 2 / 2 * sigma ^ 2)
    per_point_weight = []
    Distances = compute_distances(center, points)

    for Items in Distances:
        temp_dist = float(Items)
        temp_dist = temp_dist * temp_dist
        temp_dist = temp_dist / (2 * sigma * sigma)
        temp_dist = math.exp(-1 * temp_dist)

        per_point_weight.append(temp_dist)

    return np.array(per_point_weight) #np.array needed for testing

def compute_weighted_PCA(points, weights):

    # Copied from slide 47
    weighted_sum = np.sum(weights)
    weighted_centroid = np.sum(points * weights[:, None], axis=0) / weighted_sum
    centered = points - weighted_centroid
    cov = np.dot((centered * weights[:, None]).T, centered) / weighted_sum
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    normal = eigenvectors[:, 0]
    v = eigenvectors[:, 1]
    u = eigenvectors[:, 2]
    
    u, v, normal = enforce_viewpoint_consistency(weighted_centroid, u, v, normal)    

    return weighted_centroid, u, v, normal


def project_points_to_plane(points, centroid, U, V, W):

    temp_proj = points - centroid
    temp_proj = np.array([U,V,W]) @ np.transpose(temp_proj)
    temp_proj = np.transpose(temp_proj)

    return temp_proj

def reverse_plane_projection(projected, centroid, U, V, W):

    temp_uvw = np.array([U,V,W])
    temp_uvw = np.transpose(temp_uvw)
    temp_reverse = np.transpose(projected)
    temp_reverse = temp_uvw @ temp_reverse
    temp_reverse = np.transpose(temp_reverse)
    temp_reverse += centroid

    return temp_reverse

def make_design_matrix_A(projected):

    u = projected[:, 0]
    v = projected[:, 1]

    temp = []
    for I in range(len(projected)):
        ui = u[I]
        vi = v[I]
        temp.append([1, ui, vi, ui * ui, ui * vi, vi * vi])
    temp = np.array(temp)
    
    return temp

def make_vector_b(projected):

    temp_Vector = projected[:,-1]
    temp_Vector = np.expand_dims(temp_Vector,axis=-1)

    return temp_Vector

def make_weight_matrix_G(weights):

    temp_Matrix = np.diag(weights)

    return temp_Matrix

def compute_polynomial_coefficients(projected, weights):
    
    temp_MatA = np.array(make_design_matrix_A(projected))
    temp_VecB = np.array(make_vector_b(projected))
    temp_WeigG = np.array(make_weight_matrix_G(weights))
    
    #𝑎 = (𝐴^𝑇 𝐺 𝐴)^−1 𝐴^𝑇 𝐺 𝑏
    temp_Coef_part1 = np.linalg.inv(np.transpose(temp_MatA) @ temp_WeigG @ temp_MatA)
    temp_Coef_part2 = temp_Coef_part1 @ np.transpose(temp_MatA) @ temp_WeigG @ temp_VecB

    return temp_Coef_part2

def project_points_to_polynomial(points, centroid, U, V, W, a):

    temp_Projection = project_points_to_plane(points,centroid, U, V, W)
    temp_Designed_Mat = make_design_matrix_A(temp_Projection)
    temp_Predicted = temp_Designed_Mat @ a
    temp_Projection[:,-1] = temp_Predicted[:,-1]

    temp_Reverse = reverse_plane_projection(temp_Projection, centroid, U, V, W)

    return temp_Reverse
    
def fit_to_polynomial(center, points, sigma):

    temp_G_Weight = compute_gaussian_weights(center, points, sigma)
    temp_Centroid, temp_U, temp_V, temp_W = compute_weighted_PCA(points, temp_G_Weight)
    temp_Projected = project_points_to_plane(points, temp_Centroid, temp_U, temp_V, temp_W)
    temp_Coeff = compute_polynomial_coefficients(temp_Projected, temp_G_Weight)

    #part I am not sure
    #Project the center point only to the polynomial. 
    temp_Projected_C = project_points_to_polynomial(np.array([center]), temp_Centroid, temp_U, temp_V, temp_W, temp_Coeff)
    #Return the updated center point AND the W vector (the normal).
    return temp_Projected_C, temp_W 




